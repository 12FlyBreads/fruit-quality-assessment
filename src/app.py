# app.py
from flask import (Flask, Response, render_template_string,
                   request, jsonify)
from camera import Camera
from classifier import Classifier
from fruit_info import FruitInfo
import threading
import time
import io
from queue import Queue
from PIL import Image
from utils import MODEL_PATH, LABELS

# app innit
app = Flask(__name__)

# classes init
camera = Camera()
classifier = Classifier(MODEL_PATH, LABELS)
fruit_info = FruitInfo()

# global variables
is_classifying = False
confidence_threshold = 0.7 
classification_queue = Queue(maxsize=1) 

def classification_worker():
    """
    Loop Classification Worker
    """
    global is_classifying, confidence_threshold
    while True:
        if not is_classifying:
            time.sleep(0.1)
            continue

        try:
            jpeg_frame = camera.get_jpeg_frame()
            if jpeg_frame is None:
                continue

            img = Image.open(io.BytesIO(jpeg_frame))

            results = classifier.classify(img, confidence_threshold)

            fruit = results['fruit']['label']
            quality = results['quality']['label']
            info_text = fruit_info.get_info(fruit, quality)
            results['info'] = info_text
            
            if not classification_queue.empty():
                try:
                    classification_queue.get_nowait() 
                except Queue.Empty:
                    pass
            classification_queue.put(results)

        except Exception as e:
            print(f"Erro no worker de classificação: {e}")
        
        time.sleep(0.1) 

# --- Web Interface (HTML/JS) ---

@app.route('/')
def index():
    """ Renderiza a página principal. """
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Classificador de Frutas</title>
        <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            h1 { color: #333; }
            #video_container { 
                position: relative; 
                width: 640px; 
                margin-bottom: 10px;
            }
            img { 
                border: 2px solid #ddd; 
                border-radius: 8px; 
                width: 100%;
                height: auto;
            }
            #results_container { 
                padding: 15px; 
                background-color: #f4f4f4; 
                border-radius: 8px; 
                width: 610px; /* Alinha com a imagem */
            }
            #results_container div {
                font-size: 1.2em;
                margin-bottom: 8px;
            }
            #classification_fruit { font-weight: bold; }
            #classification_quality { font-style: italic; }
            #fruit_info { color: #555; }
            .controls button {
                font-size: 1em; padding: 10px 15px; margin-right: 10px;
                border: none; border-radius: 5px; cursor: pointer;
            }
            #startBtn { background-color: #4CAF50; color: white; }
            #stopBtn { background-color: #f44336; color: white; }
            #stopBtn:disabled { background-color: #ccc; }
        </style>
        <script>
            function startClassification() {
                $.post('/start');
                $('#startBtn').prop('disabled', true);
                $('#stopBtn').prop('disabled', false);
            }
            function stopClassification() {
                $.post('/stop');
                $('#startBtn').prop('disabled', false);
                $('#stopBtn').prop('disabled', true);
            }
            function updateConfidence() {
                var confidence = $('#confidence').val();
                $.post('/update_confidence', {confidence: confidence});
            }
            
            // Função que busca os resultados da classificação
            function updateClassificationResults() {
                $.get('/get_classification', function(data) {
                    if (data.message) {
                        // Se não estiver classificando
                        $('#classification_fruit').text(data.message);
                        $('#classification_quality').text('');
                        $('#fruit_info').text('');
                    } else if (data.fruit) {
                        // Se estiver classificando
                        var fruit_text = `Fruta: ${data.fruit.label} (${(data.fruit.probability * 100).toFixed(1)}%)`;
                        var quality_text = `Qualidade: ${data.quality.label} (${(data.quality.probability * 100).toFixed(1)}%)`;
                        var info_text = `Info: ${data.info}`;
                        
                        $('#classification_fruit').text(fruit_text);
                        $('#classification_quality').text(quality_text);
                        $('#fruit_info').text(info_text);
                    }
                });
            }
            
            // Inicia o polling quando o documento estiver pronto
            $(document).ready(function() {
                setInterval(updateClassificationResults, 200); // Atualiza 5x por segundo
            });
        </script>
    </head>
    <body>
        <h1>Classificador de Frutas e Qualidade</h1>
        <div id="video_container">
            <img src="{{ url_for('video_feed') }}" width="640" height="480" />
        </div>
        
        <div class="controls">
            <button id="startBtn" onclick="startClassification()">Iniciar Classificação</button>
            <button id="stopBtn" onclick="stopClassification()" disabled>Parar Classificação</button>
        </div>
        
        <br>
        <label for="confidence">Limiar de Confiança:</label>
        <input type="number" id="confidence" name="confidence" min="0" max="1" step="0.05" value="0.7" onchange="updateConfidence()" />
        
        <hr>
        <div id="results_container">
            <div id="classification_fruit">Aguardando início...</div>
            <div id="classification_quality"></div>
            <div id="fruit_info"></div>
        </div>
    </body>
    </html>
    ''')

# --- Endpoints da API ---

@app.route('/video_feed')
def video_feed():
    """ Rota de streaming de vídeo. """
    return Response(camera.stream_generator(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/start', methods=['POST'])
def start_classification():
    """ Inicia o processo de classificação. """
    global is_classifying
    is_classifying = True
    print("Classificação iniciada.")
    return '', 204

@app.route('/stop', methods=['POST'])
def stop_classification():
    """ Para o processo de classificação. """
    global is_classifying
    is_classifying = False
    print("Classificação parada.")
    return '', 204

@app.route('/update_confidence', methods=['POST'])
def update_confidence():
    """ Atualiza o limiar de confiança. """
    global confidence_threshold
    confidence_threshold = float(request.form['confidence'])
    print(f"Limiar de confiança atualizado para: {confidence_threshold}")
    return '', 204

@app.route('/get_classification')
def get_classification():
    """ Rota de polling para obter o último resultado da classificação. """
    if not is_classifying:
        return jsonify({'message': 'Classificação parada.'})
    
    try:
        # Pega o último resultado da fila sem bloquear
        result = classification_queue.get_nowait()
        return jsonify(result)
    except Queue.Empty:
        # Se a fila estiver vazia (processando)
        return jsonify({'message': 'Processando...'})

# --- Execução ---

if __name__ == '__main__':
    try:
        threading.Thread(target=classification_worker, daemon=True).start()
        
        print("Servidor Flask iniciado em http://0.0.0.0:5000")

        app.run(host='0.0.0.0', port=5000, threaded=True)
        
    except KeyboardInterrupt:
        print("Desligando...")
    finally:
        camera.stop() 
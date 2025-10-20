# classifier.py
import tflite_runtime.interpreter as tflite
import numpy as np
from PIL import Image

class Classifier:
    def __init__(self, model_path, labels) -> None:
        """
        Iniatilize the Classifier with the given TFLite model and labels.
        :param model_path: Path to the TFLite model file.
        :param labels: List of labels corresponding to model outputs.
        :return: None
        """

        print("Loading model...")
        self.interpreter = self._load_model(model_path)
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()
        self.labels = labels

        print("Model loaded.")

    def _load_model(self, model_path) -> tflite.Interpreter:
        """ 
        Load a TFLite model and allocate tensors. 
        :param model_path: Path to the TFLite model file.
        :return: Allocated TFLite Interpreter instance.
        """
        interpreter = tflite.Interpreter(model_path=model_path)
        interpreter.allocate_tensors()
        return interpreter

    def _run_inference(self, img, interpreter, input_details, output_details) -> np.ndarray:
        """ 
        Execute inference on a specific model. 
        :param img: PIL Image to classify.
        :param interpreter: TFLite Interpreter instance.
        :param input_details: Input details from the interpreter.
        :param output_details: Output details from the interpreter.
        :return: Numpy array of predictions.
        """

        input_shape = input_details[0]['shape']
        height, width = input_shape[1], input_shape[2] 
        img_resized = img.resize((width, height))
        
        input_data = np.expand_dims(img_resized, axis=0)
        
        input_dtype = input_details[0]['dtype']
        if input_dtype == np.uint8 or input_dtype == np.int8:
            input_data = input_data.astype(input_dtype)

        interpreter.set_tensor(input_details[0]['index'], input_data)
        interpreter.invoke()
        
        predictions = interpreter.get_tensor(output_details[0]['index'])[0]
        
        output_dtype = output_details[0]['dtype']
        if output_dtype == np.uint8 or output_dtype == np.int8:
            scale, zero_point = output_details[0]['quantization']
            predictions = (predictions.astype(np.float32) - zero_point) * scale
        
        return predictions

    def classify(self, img, confidence_threshold) -> dict:
        """
        Classifies an image and splits the label.
        :param img: PIL Image to classify.
        :param confidence_threshold: Minimum confidence to accept a prediction.
        :return: Dictionary with 'fruit' and 'quality' information.
        """

        preds = self._run_inference(img, self.interpreter,
                                    self.input_details,
                                    self.output_details)

        # Process the result
        prob = np.max(preds)
        
        if prob >= confidence_threshold:
            label_index = np.argmax(preds)
            combined_label = self.labels[label_index]
            
            parts = combined_label.split(' ')
            if len(parts) >= 2:
                quality_label = parts[0]    
                fruit_label = ' '.join(parts[1:])  
            else:
                quality_label = 'N/A'
                fruit_label = combined_label

        else:
            quality_label = 'Indefinida'
            fruit_label = 'Desconhecido'
            prob = 1.0

        return {
            'fruit': {
                'label': fruit_label,
                'probability': float(prob)
            },
            'quality': {
                'label': quality_label,
                'probability': float(prob)
            }
        }
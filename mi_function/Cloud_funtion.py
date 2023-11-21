import json
from google.cloud import storage, firestore

storage_client = storage.Client()
firestore_client = firestore.Client()

def read_json_from_gcs(event, context):
    # Obtener el nombre del archivo JSON creado en Cloud Storage
    bucket_name = "mi-bucket-proyecto"
    file_name = event['name']

    # Obtener el objeto JSON desde Cloud Storage
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    content = blob.download_as_text()

    # Convertir el JSON a un diccionario de Python
    data = json.loads(content)

    # Obtener el contador actual desde Firestore
    counter_doc_ref = firestore_client.collection("counters").document("registro-counter")
    counter_data = counter_doc_ref.get().to_dict()

    if counter_data is None:
        # Si el contador no existe, lo inicializa en 1
        counter_value = 1
    else:
        # Si el contador existe, incrementa su valor
        counter_value = counter_data.get("value", 1) + 1

    # Actualizar el contador en Firestore
    counter_doc_ref.set({"value": counter_value})

    # Construir el nombre descriptivo del registro
    registro_name = f"registro-{counter_value}"

    # Guardar los datos en Firestore con el nombre descriptivo
    collection_name = "bbdd-gcp" 
    firestore_client.collection(collection_name).document(registro_name).set(data)

    print(f"Datos guardados correctamente en la bbdd como {registro_name}")
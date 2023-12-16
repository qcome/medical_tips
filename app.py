from flask import Flask, render_template, request, jsonify
import openai
import json

openai.api_key = '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'

app = Flask(__name__)

def load_json_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

@app.route('/')
def index():
    symptoms_data = load_json_data('symptoms.json')
    body_parts = load_json_data('body_parts.json')
    return render_template('index.html', symptoms_data=symptoms_data, body_parts=body_parts)

@app.route('/diagnose', methods=['POST'])
def diagnose():
    form_data = request.form
    selected_symptoms = form_data['specific_symptoms'].split(',')
    symptoms_str = ", ".join(selected_symptoms)

    prompt = f"Tu es un expert en médecine. Patient: Âge: {form_data['age']}, Sexe: {form_data['sex']}, Antécédents médicaux: {form_data['medical_history']}. Symptômes: {symptoms_str}, Description: {form_data['description']}. Quel serait ton diagnostic et recommandations ?"
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": prompt},
        ]
    )

    if response.choices:
        return jsonify(diagnosis=response.choices[0].message.content)
    else:
        return jsonify(diagnosis="Aucune réponse")

if __name__ == '__main__':
    app.run(debug=True)

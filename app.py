from flask import Flask, render_template, request, jsonify
import spacy

app = Flask(__name__)

# โหลดโมเดลภาษาอังกฤษของ Spacy
nlp = spacy.load('en_core_web_sm')

unwanted_words = [
    'within', 'often', 'also', 'example',
    'form', 'value', 'large', 'group', 'base', 'likely',
    'and', 'is', 'of', 'in', 'to', 'with', 'for', 'as', 'on', 'by', 'at', 'we', 'make', 'well', 'would',
    'from', 'it', 'have', 'about', 'something', 'thing', 'everything', 'anything',
    'refer', 'indicate', 'occur', 'allow', 'pick', 'forecasting', 'tool', 'result',
    'present', 'certain', 'set', 'apply', 'do', 'well', 'another',
    'pair', 'correlation', 'represented', 'side', 'search', 'together', 'b'
    'mean', 'hide', 'seek', 'take'
]

rules = {
        'Rule': 'relationship',
        'relationship': 'rules',

        'Relationship': 'data',
        'data': 'Relationship',

        'Product': 'relationship',
        'relationship': 'Product',

        'Use': 'rule',
        'rule': 'Use',

        'Purchase': 'relationship',
        'relationship': 'Purchase', 

        'relationship': 'find', 
        'find': 'relationship', 

        'data': 'find', 
        'find': 'data', 

        'relationship': 'find', 
        'find': 'relationship', 
    }

def preprocess_text(text):
    doc = nlp(text)
    filtered_words = [token.text for token in doc if token.text.lower() not in unwanted_words]
    return filtered_words

def calculate_score(answer):
    score = 0
    processed_answer = preprocess_text(answer)
    for word in processed_answer:
        if word in rules.keys():
            score += 1
    if score >= 3:
        return 5
    elif score == 2:
        return 4
    elif score == 1:
        return 3
    else:
        return 0

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/score', methods=['POST'])
def score():
    data = request.get_json()
    answer = data['testText']

    test_text = request.form['testText']  # รับข้อความจากแบบฟอร์ม
    image_file = request.files['imageInput']  # รับไฟล์รูปภาพจากแบบฟอร์ม
    
    score = calculate_score(answer)
    return jsonify({'score': score})

if __name__ == '__main__':
    app.run(debug=True)

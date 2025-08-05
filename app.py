# app.py
from flask import Flask, render_template, request
from scraper import scrape_delhi_high_court

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        case_type = request.form['case_type']
        case_number = request.form['case_number']
        filing_year = request.form['filing_year']

        try:
            result, pdf_links = scrape_delhi_high_court(case_type, case_number, filing_year)
            return render_template('result.html', case_data=result, pdf_links=pdf_links)
        except Exception as e:
            return render_template('result.html', error=str(e))

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

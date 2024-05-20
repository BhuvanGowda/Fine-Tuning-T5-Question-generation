# -*- coding: utf-8 -*-
"""QuestionGenration.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1QgNe3JyNclOkEFu-4F5DYnZBbRWA26iJ

## This codes depicts Fine tuning of T5 model for question genration task

Input: Path of pdf for which questions need to be generate, and path where generated questions pdf needs tpo be stored

output: Pdf file containg all the questions generated.

Model: BhuvanGowda/t5-small-finetuned-QuestionGen

Link to model: https://huggingface.co/BhuvanGowda/t5-small-finetuned-QuestionGen/commit/3886dc3777fd04c6578f19a1c7cb8cbe817d22b1

For more details of fine tuning refer below!

# Context: link to fine tuning of T5 model

link: https://colab.research.google.com/drive/1GkXtFCn1S-WQIjcIny9p4EkQj1ESCuh7?usp=sharing
"""

#Insatall pymupdf & reportlab
!pip install --upgrade pymupdf --upgrade reportlab

#Importing necessary Packages
import pymupdf as py
from transformers import pipeline
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

#Function extract_text_from_pdf: Data pipeline for Question genration task & returns List of questions genrated
def extract_text_from_pdf(pdf_path):#Input: Path of the pdf to be processed
    text = "" #empty string to store extracted text
    pdf_document = py.open(pdf_path)
    for page_num in range(len(pdf_document)):
        page = pdf_document[page_num]
        text += page.get_text()
    pdf_document.close()

    #returning the extracted text
    return text

#Function generate_questions: Data pipeline for Question genration task & returns List of questions genrated
def generate_questions(text, model, tokenizer, max_length=512): #Input: text extracted, Model, Tokenizer, Maximum length of segment to be considered while genration.
    question_generator = pipeline("text2text-generation", model=model, tokenizer=tokenizer) #Creating pipeline
    generated_questions = set()  # Use a set to store unique questions

    # Split text into segments
    text_segments = [text[i:i+max_length] for i in range(0, len(text), max_length)]

    #Question Gentarion happens here
    for segment in text_segments:
        if segment.strip():  # Ensure segment is not empty
            #Question genrated
            questions = question_generator(segment, num_return_sequences=1) #num_return_sequences specifies the number of questions function has to generate
            for q in questions:
              #Adding the question genrated to the list of generated questions
              generated_questions.add(q['generated_text'])

    #Returning List containing the questions generated
    return list(generated_questions)

#Function save_questions_to_pdf: Saves the genrated questions into a downloadable Pdf file
def save_questions_to_pdf(questions, output_pdf_path): #input List of questions genrated & path where the pdf has to be saved
    pdf = canvas.Canvas(output_pdf_path, pagesize=letter)
    pdf.setFont("Helvetica", 12)

    for i, question in enumerate(questions, 1):
        try:
            pdf.drawString(50, 750 - i * 20, f"Question {i}: {question}")
        except Exception as e:
            print(f"Error processing question {i}: {e}")

    pdf.save()

#Main function
if __name__ == "__main__":

    # Specify the path to your PDF file
    pdf_path = r"/content/Document.pdf"

    # Specify the output PDF file path
    output_pdf_path = r"/content/generated_questions.pdf"

    # Extract text from PDF
    pdf_text = extract_text_from_pdf(pdf_path)



    #initaializing Model and tokenizer
    #Link to model: https://huggingface.co/BhuvanGowda/t5-small-finetuned-QuestionGen/commit/3886dc3777fd04c6578f19a1c7cb8cbe817d22b1

    #Initializing Model from hugging face
    model = AutoModelForSeq2SeqLM.from_pretrained("BhuvanGowda/t5-small-finetuned-QuestionGen")

    #Initializing tokenizer
    tokenizer = AutoTokenizer.from_pretrained("BhuvanGowda/t5-small-finetuned-QuestionGen")



    if pdf_text: #checling for extracted text is not empty

        # Generate questions from extracted text
        generated_questions = generate_questions(text = pdf_text, model = model,tokenizer=tokenizer)

        if generated_questions: #checling for Questions generated is not empty
            #Printing Quesrions Generated
            print("Generated Questions:")
            for i, question in enumerate(generated_questions, 1):
                print(f"Question {i}: {question}")

            # Save generated questions to a PDF file
            save_questions_to_pdf(generated_questions, output_pdf_path)
            print(f"Generated questions saved to: {output_pdf_path}")

        else:
            print("No questions generated.")

    else:
        print("Failed to extract text from PDF.")

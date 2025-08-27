from rest_framework.response import Response
from rest_framework.decorators import api_view
from .utils import (
	extract_text_from_pdf,
	extract_text_from_docx,
	store_document,
	get_document,
	get_next_doc_id,
	get_openai_answer
)



@api_view(["POST"])
def upload_document(request):
	uploaded_files = request.FILES.getlist("files")
	if not uploaded_files:
		return Response({"error": "No files uploaded"}, status=400)

	combined_text = ""
	for uploaded_file in uploaded_files:
		if uploaded_file.name.endswith(".pdf"):
			combined_text += extract_text_from_pdf(uploaded_file) + "\n"
		elif uploaded_file.name.endswith(".docx") or uploaded_file.name.endswith(".doc"):
			combined_text += extract_text_from_docx(uploaded_file) + "\n"
		else:
			return Response({"error": f"Unsupported file type: {uploaded_file.name}"}, status=400)


	doc_id = request.user.id
	store_document(doc_id, combined_text)

	return Response({"message": "Files uploaded successfully"}, status=201)


@api_view(["POST"])
def chat_with_doc(request):
	doc_id = request.user.id
	question = request.data.get("question")

	if not doc_id or not question:
		return Response({"error": "doc_id and question required"}, status=400)

	document_text = get_document(doc_id)
	if not document_text:
		return Response({"error": "Document not found"}, status=404)

	answer = get_openai_answer(document_text, question)
	return Response({"answer": answer}, status=200)

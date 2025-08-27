from django.http import JsonResponse
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
	uploaded_file = request.FILES.get("file")
	if not uploaded_file:
		return JsonResponse({"error": "No file uploaded"}, status=400)

	if uploaded_file.name.endswith(".pdf"):
		text = extract_text_from_pdf(uploaded_file)
	elif uploaded_file.name.endswith(".docx") or uploaded_file.name.endswith(".doc"):
		text = extract_text_from_docx(uploaded_file)
	else:
		return JsonResponse({"error": "Unsupported file type"}, status=400)

	doc_id = get_next_doc_id()
	store_document(doc_id, text)

	return JsonResponse({"message": "File uploaded successfully", "doc_id": doc_id})


@api_view(["POST"])
def chat_with_doc(request):
	doc_id = request.data.get("doc_id")
	question = request.data.get("question")

	if not doc_id or not question:
		return JsonResponse({"error": "doc_id and question required"}, status=400)

	document_text = get_document(doc_id)
	if not document_text:
		return JsonResponse({"error": "Document not found"}, status=404)

	answer = get_openai_answer(document_text, question)
	return JsonResponse({"answer": answer})

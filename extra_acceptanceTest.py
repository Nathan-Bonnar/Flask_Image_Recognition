"""Acceptance tests for image uploads to the Flask prediction endpoint."""
from io import BytesIO



def test_happy_multiple_image_formats_jpeg(client):
    """
    Happy Test Case: Upload of JPEG Format Image
    - Purpose: Verify system accepts JPEG format images and returns prediction.
    - Method:
        - Create mock JPEG image data with proper header.
        - POST to prediction endpoint.
        - Assert successful response with prediction.
    """
    # Minimal valid JPEG header + data
    jpeg_data = b'\xff\xd8\xff\xe0' + b'JFIF\x00' + b'image_data_here'
    jpeg_file = BytesIO(jpeg_data)
    jpeg_file.name = "test_image.jpg"

    response = client.post(
        "/prediction",
        data={"file": (jpeg_file, jpeg_file.name)},
        content_type="multipart/form-data"
    )

    assert response.status_code == 200
    assert b"Prediction" in response.data


def test_happy_multiple_image_formats_png(client):
    """
    Happy Test Case: Upload of PNG Format Image
    - Purpose: Verify system accepts PNG format images and returns prediction.
    - Method:
        - Create mock PNG image data with proper header.
        - POST to prediction endpoint.
        - Assert successful response with prediction.
    """
    # Minimal valid PNG header + data
    png_data = b'\x89PNG\r\n\x1a\n' + b'image_data_here'
    png_file = BytesIO(png_data)
    png_file.name = "test_image.png"

    response = client.post(
        "/prediction",
        data={"file": (png_file, png_file.name)},
        content_type="multipart/form-data"
    )

    assert response.status_code == 200
    assert b"Prediction" in response.data


def test_happy_multiple_image_formats_webp(client):
    """
    Happy Test Case: Upload of WEBP Format Image
    - Purpose: Verify system accepts WEBP format images and returns prediction.
    - Method:
        - Create mock WEBP image data with proper header.
        - POST to prediction endpoint.
        - Assert successful response with prediction.
    """
    # Minimal valid WEBP header (RIFF header with WEBP signature)
    webp_data = b'RIFF' + b'\x00\x00\x00\x00' + b'WEBP' + b'image_data_here'
    webp_file = BytesIO(webp_data)
    webp_file.name = "test_image.webp"

    response = client.post(
        "/prediction",
        data={"file": (webp_file, webp_file.name)},
        content_type="multipart/form-data"
    )

    assert response.status_code == 200
    assert b"Prediction" in response.data


def test_sad_unsupported_pdf_format(client):
    """
    Sad Test Case: Upload of PDF File Format
    - Purpose: Verify system rejects PDF files with appropriate error.
    - Method:
        - Create a PDF file with proper header.
        - POST to prediction endpoint.
        - Assert error response or graceful handling.
    """
    # PDF header
    pdf_data = b'%PDF-1.4' + b'This is a PDF file content'
    pdf_file = BytesIO(pdf_data)
    pdf_file.name = "document.pdf"

    response = client.post(
        "/prediction",
        data={"file": (pdf_file, pdf_file.name)},
        content_type="multipart/form-data"
    )

    # Should not return 200 with prediction for non-image file
    if response.status_code == 200:
        assert b"error" in response.data.lower() or b"invalid" in response.data.lower()
    else:
        assert response.status_code in [400, 415, 422]  # Appropriate error codes


def test_sad_unsupported_txt_format(client):
    """
    Sad Test Case: Upload of Text File Format
    - Purpose: Verify system rejects plain text files with appropriate error.
    - Method:
        - Create a text file with content.
        - POST to prediction endpoint.
        - Assert error response or graceful handling.
    """
    text_data = b"This is a plain text file content, not an image."
    text_file = BytesIO(text_data)
    text_file.name = "document.txt"

    response = client.post(
        "/prediction",
        data={"file": (text_file, text_file.name)},
        content_type="multipart/form-data"
    )

    # Should not return 200 with prediction for non-image file
    if response.status_code == 200:
        assert b"error" in response.data.lower() or b"invalid" in response.data.lower()
    else:
        assert response.status_code in [400, 415, 422]  # Appropriate error codes


def test_sad_unsupported_xml_format(client):
    """
    Sad Test Case: Upload of XML File Format
    - Purpose: Verify system rejects XML files with appropriate error.
    - Method:
        - Create an XML file with proper structure.
        - POST to prediction endpoint.
        - Assert error response or graceful handling.
    """
    xml_data = b'<?xml version="1.0"?><root><data>This is XML</data></root>'
    xml_file = BytesIO(xml_data)
    xml_file.name = "data.xml"

    response = client.post(
        "/prediction",
        data={"file": (xml_file, xml_file.name)},
        content_type="multipart/form-data"
    )

    # Should not return 200 with prediction for non-image file
    if response.status_code == 200:
        assert b"error" in response.data.lower() or b"invalid" in response.data.lower()
    else:
        assert response.status_code in [400, 415, 422]  # Appropriate error codes


def test_sad_corrupted_jpeg_file(client):
    """
    Sad Test Case: Upload of Corrupted JPEG File
    - Purpose: Verify system handles corrupted JPEG files gracefully.
    - Method:
        - Create a corrupted JPEG file (valid header but truncated data).
        - POST to prediction endpoint.
        - Assert error response or graceful handling.
    """
    # Valid JPEG header but corrupted/incomplete data
    corrupted_jpeg = b'\xff\xd8\xff\xe0' + b'JFIF\x00' + b'incomplete_data'
    corrupted_file = BytesIO(corrupted_jpeg)
    corrupted_file.name = "corrupted.jpg"

    response = client.post(
        "/prediction",
        data={"file": (corrupted_file, corrupted_file.name)},
        content_type="multipart/form-data"
    )

    # Should handle gracefully without crashing
    assert response.status_code != 500
    if response.status_code == 200:
        assert b"error" in response.data.lower() or b"corrupt" in response.data.lower()


def test_sad_corrupted_png_file(client):
    """
    Sad Test Case: Upload of Corrupted PNG File
    - Purpose: Verify system handles corrupted PNG files gracefully.
    - Method:
        - Create a corrupted PNG file (valid header but missing chunks).
        - POST to prediction endpoint.
        - Assert error response or graceful handling.
    """
    # Valid PNG header but missing required chunks
    corrupted_png = b'\x89PNG\r\n\x1a\n' + b'incomplete_png_data'
    corrupted_file = BytesIO(corrupted_png)
    corrupted_file.name = "corrupted.png"

    response = client.post(
        "/prediction",
        data={"file": (corrupted_file, corrupted_file.name)},
        content_type="multipart/form-data"
    )

    # Should handle gracefully without crashing
    assert response.status_code != 500
    if response.status_code == 200:
        assert b"error" in response.data.lower() or b"corrupt" in response.data.lower()


def test_sad_corrupted_webp_file(client):
    """
    Sad Test Case: Upload of Corrupted WEBP File
    - Purpose: Verify system handles corrupted WEBP files gracefully.
    - Method:
        - Create a corrupted WEBP file (valid header but incomplete data).
        - POST to prediction endpoint.
        - Assert error response or graceful handling.
    """
    # Valid WEBP header but incomplete data
    corrupted_webp = b'RIFF' + b'\x00\x00\x00\x00' + b'WEBP' + b'incomplete_webp_data'
    corrupted_file = BytesIO(corrupted_webp)
    corrupted_file.name = "corrupted.webp"

    response = client.post(
        "/prediction",
        data={"file": (corrupted_file, corrupted_file.name)},
        content_type="multipart/form-data"
    )

    # Should handle gracefully without crashing
    assert response.status_code != 500
    if response.status_code == 200:
        assert b"error" in response.data.lower() or b"corrupt" in response.data.lower()


from dash import Dash, html, dcc, Output, Input
from ironpdf import ChromePdfRenderer, License

# Apply your IronPDF license key
License.LicenseKey = "IRONSUITE.VIOAVILA23.GMAIL.COM.1641-FDC000F752-BAVU4FV6NYVVGQ-7IIE4LNSISKX-SKAZLSGLUEIO-WWDMRR7W3UCY-JF6W4CIJD4HR-4W3ZN42NXRS5-DCOB2H-TN65HXEVHTGOEA-DEPLOYMENT.TRIAL-D56XSP.TRIAL.EXPIRES.04.JAN.2025"

# Initialize Dash app
app = Dash(__name__)

# Define the app layout
app.layout = html.Div(
    [
        html.H1("Generate PDF", style={"textAlign": "center"}),
        html.Button("Generate PDF", id="generate-pdf-button", n_clicks=0, style={"margin": "20px", "padding": "10px 20px", "fontSize": "16px"}),
        html.Div(id="pdf-status", style={"textAlign": "center", "marginTop": "20px", "fontSize": "18px"}),
    ]
)

# Callback to handle PDF generation when the button is clicked
@app.callback(
    Output("pdf-status", "children"),
    Input("generate-pdf-button", "n_clicks"),
)
def generate_pdf(n_clicks):
    if n_clicks == 0:
        return ""  # No action on initial page load

    try:
        # Generate the PDF using IronPDF
        renderer = ChromePdfRenderer()
        pdf = renderer.RenderUrlAsPdf("http://127.0.0.1:8050/")
        save_path = "C:/Users/viomi/Downloads/output.pdf"  # Specify the save location
        pdf.SaveAs(save_path)

        # Return success message
        return f"PDF generated successfully and saved to: {save_path}"

    except Exception as e:
        # Return error message
        return f"An error occurred while generating the PDF: {str(e)}"


# Run the Dash app
if __name__ == "__main__":
    app.run_server(debug=True)

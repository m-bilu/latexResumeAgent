import streamlit as st
import tempfile
import subprocess
from pathlib import Path
from streamlit_pdf_viewer import pdf_viewer

from graph import modify_resume


def render_pdf(latex_code: str) -> bytes:
    with tempfile.TemporaryDirectory() as tmpdir:
        tex_path = Path(tmpdir) / "resume.tex"
        pdf_path = tex_path.with_suffix(".pdf")
        
        with open(tex_path, "w") as f:
            f.write(latex_code)
        
        print(f"Temp directory before pdflatex: {tmpdir}")
        print("Contents before:", list(Path(tmpdir).iterdir()))
        
        try:
            command = ["pdflatex", "-interaction=nonstopmode", str(tex_path)]
            print(command)

            subprocess.run(
                command,
                cwd=tmpdir
            )
            
            print(f"Temp directory after pdflatex: {tmpdir}")
            print("Contents after:", list(Path(tmpdir).iterdir()))
            
            with open(pdf_path, "rb") as f:
                return f.read()
        except subprocess.CalledProcessError:
            print(f"pdflatex command failed in directory: {tmpdir}")
            return None
        

st.title("🧠 LaTeX Resume Tailoring Tool")

st.markdown("Upload your resume and a job description. We'll tailor your resume using AI to improve your chances.")

uploaded_tex = st.file_uploader("Upload your LaTeX resume (.tex)", type=["tex"])
job_description = st.text_area("Paste the job description here")

if uploaded_tex and job_description:
    old_tex_code = uploaded_tex.read().decode("utf-8")

    st.subheader("📄 Original Resume (PDF)")
    old_pdf = render_pdf(old_tex_code)
    if old_pdf:
        st.download_button("Download Original PDF", data=old_pdf, file_name="original_resume.pdf")
        pdf_viewer(old_pdf)
    else:
        st.error("Failed to render original LaTeX as PDF.")

    if st.button("✏️ Generate Edited Resume"):
        st.info("Generating edited resume...")

        edited_tex_code = modify_resume(old_tex_code, job_description)

        st.subheader("✅ Edited Resume (PDF)")
        new_pdf = render_pdf(edited_tex_code)
        if new_pdf:
            st.download_button("Download Edited PDF", data=new_pdf, file_name="edited_resume.pdf")
            st.download_button("Download Edited LaTeX", data=edited_tex_code, file_name="edited_resume.tex")
            pdf_viewer(new_pdf)
        else:
            st.error("Failed to render edited LaTeX as PDF.")

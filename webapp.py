import streamlit as st
import yt_dlp
import os

st.set_page_config(page_title="Jidan Video Downloader", page_icon="📥")
st.title("📥 Social Media Video Downloader")
st.markdown("Developed by **HABIBULLAH JIDAN**")

url = st.text_input("ভিডিও লিঙ্কটি এখানে পেস্ট করুন:")

if url:
    try:
        # কুকি ফাইল চেক করা
        cookie_path = 'cookies.txt' if os.path.exists('cookies.txt') else None

        ydl_opts_info = {
            'quiet': True,
            'cookiefile': cookie_path, # এখানে কুকি ব্যবহার করা হচ্ছে
            'nocheckcertificate': True,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
        }

        with yt_dlp.YoutubeDL(ydl_opts_info) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = info.get('formats', [])
            res_options = {f"{f['height']}p - {f['ext']}": f['format_id'] for f in formats if f.get('height')}

            selected_label = st.selectbox("রেজোলিউশন সিলেক্ট করুন:", list(res_options.keys()))

            if st.button("Download Video"):
                st.info("প্রসেসিং হচ্ছে...")
                out_filename = "final_video.mp4"
                
                ydl_opts_final = {
                    'format': f"{res_options[selected_label]}+bestaudio/best",
                    'outtmpl': out_filename,
                    'merge_output_format': 'mp4',
                    'cookiefile': cookie_path, # ডাউনলোডের সময়ও কুকি লাগবে
                    'nocheckcertificate': True,
                }

                with yt_dlp.YoutubeDL(ydl_opts_final) as ydl:
                    ydl.download([url])
                
                with open(out_filename, "rb") as file:
                    st.download_button(label="সেভ করুন", data=file, file_name="video.mp4", mime="video/mp4")
                os.remove(out_filename)

    except Exception as e:
        st.error(f"Error: {str(e)}")

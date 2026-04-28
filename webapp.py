import streamlit as st
import yt_dlp
import os

# পেজ সেটআপ
st.set_page_config(page_title="Jidan Video Downloader", page_icon="📥")

st.title("📥 Social Media Video Downloader")
st.markdown("Developed by **HABIBULLAH JIDAN**")

# লিঙ্ক ইনপুট
url = st.text_input("ভিডিও লিঙ্কটি এখানে পেস্ট করুন:", placeholder="https://www.youtube.com/watch?v=...")

if url:
    try:
        with yt_dlp.YoutubeDL() as ydl:
            info = ydl.extract_info(url, download=False)
            formats = info.get('formats', [])
            
            # রেজোলিউশন লিস্ট তৈরি
            res_options = {}
            for f in formats:
                if f.get('vcodec') != 'none' and f.get('height'):
                    label = f"{f['height']}p - {f['ext']} ({f.get('filesize_approx', 0)//(1024*1024)} MB)"
                    res_options[label] = f['format_id']

            selected_res = st.selectbox("রেজোলিউশন সিলেক্ট করুন:", list(res_options.keys()))

            if st.button("Download Video"):
                st.info("প্রসেসিং হচ্ছে... কিছুক্ষণ অপেক্ষা করুন।")
                
                # ডাউনলোড সেটিংস
                out_filename = "downloaded_video.mp4"
                ydl_opts = {
                    'format': f"{res_options[selected_res]}+bestaudio/best",
                    'outtmpl': out_filename,
                    'merge_output_format': 'mp4',
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                
                # ওয়েবসাইট থেকে ডাউনলোডের জন্য ফাইল রিড করা
                with open(out_filename, "rb") as file:
                    st.download_button(
                        label="Click to Save to Device",
                        data=file,
                        file_name=f"{info['title']}.mp4",
                        mime="video/mp4"
                    )
                os.remove(out_filename) # সার্ভার থেকে ফাইল ডিলিট করা

    except Exception as e:
        st.error(f"Error: {e}")

# ফূটার
st.markdown("---")
st.markdown("[Contact Developer on Facebook](https://www.facebook.com/profile.php?id=100087711907484)")
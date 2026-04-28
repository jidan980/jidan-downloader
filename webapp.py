import streamlit as st
import yt_dlp
import os

# ১. গুগল সার্চ কনসোল ভেরিফিকেশন কোড (এটি গুগলের জন্য)
st.markdown(
    '<meta name="google-site-verification" content="q37wfxmAjum4zP66LO3lWE2eiyI7nfdSFEACOSW3TRc" />', 
    unsafe_allow_html=True
)

# ২. পেজ সেটআপ এবং সার্চ ইঞ্জিনের জন্য কিওয়ার্ড
st.set_page_config(
    page_title="Jidan Downloader - Best Free Video Downloader", 
    page_icon="📥", 
    layout="centered"
)

# ৩. ব্র্যান্ডিং এবং টাইটেল
st.title("📥 Social Media Video Downloader")
st.markdown("Developed by **HABIBULLAH JIDAN**")

# ৪. ভিডিও লিঙ্ক ইনপুট
url = st.text_input("ভিডিও লিঙ্কটি এখানে পেস্ট করুন:", placeholder="https://www.youtube.com/watch?v=...")

if url:
    try:
        # কুকি ফাইল থাকলে সেটি ব্যবহার করা (403 Error এড়াতে)
        cookie_path = 'cookies.txt' if os.path.exists('cookies.txt') else None

        ydl_opts_info = {
            'quiet': True,
            'no_warnings': True,
            'cookiefile': cookie_path,
            'nocheckcertificate': True,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
        }

        with yt_dlp.YoutubeDL(ydl_opts_info) as ydl:
            # ভিডিও তথ্য সংগ্রহ
            info = ydl.extract_info(url, download=False)
            formats = info.get('formats', [])
            title = info.get('title', 'video')
            
            # রেজোলিউশন লিস্ট তৈরি
            res_options = {}
            for f in formats:
                if f.get('vcodec') != 'none' and f.get('height'):
                    res = f.get('height')
                    ext = f.get('ext')
                    filesize = f.get('filesize') or f.get('filesize_approx') or 0
                    size_mb = f"{filesize/(1024*1024):.1f} MB"
                    
                    label = f"{res}p - {ext} ({size_mb})"
                    res_options[label] = f['format_id']

            # ড্রপডাউন মেনু
            selected_label = st.selectbox("রেজোলিউশন সিলেক্ট করুন:", list(res_options.keys()))

            if st.button("Download Video"):
                st.info("প্রসেসিং হচ্ছে... কিছুক্ষণ অপেক্ষা করুন।")
                
                out_filename = "final_video.mp4"
                ydl_opts_final = {
                    'format': f"{res_options[selected_label]}+bestaudio/best",
                    'outtmpl': out_filename,
                    'merge_output_format': 'mp4',
                    'cookiefile': cookie_path,
                    'nocheckcertificate': True,
                    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
                }

                with yt_dlp.YoutubeDL(ydl_opts_final) as ydl:
                    ydl.download([url])
                
                # ডাউনলোড বাটন দেখানো
                if os.path.exists(out_filename):
                    with open(out_filename, "rb") as file:
                        st.success("ভিডিওটি এখন ডাউনলোডের জন্য প্রস্তুত!")
                        st.download_button(
                            label="ফাইলটি সেভ করতে এখানে ক্লিক করুন",
                            data=file,
                            file_name=f"{title}.mp4",
                            mime="video/mp4"
                        )
                    # সার্ভার থেকে ফাইল ডিলিট করা
                    os.remove(out_filename)

    except Exception as e:
        st.error(f"দুঃখিত, একটি সমস্যা হয়েছে। দয়া করে সঠিক লিঙ্ক ব্যবহার করুন।")

# ৫. ফূটার সেকশন
st.markdown("---")
st.markdown(f"© 2026 **HABIBULLAH JIDAN** | [Contact on Facebook](https://www.facebook.com/profile.php?id=100087711907484)")

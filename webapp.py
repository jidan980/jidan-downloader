import streamlit as st
import yt_dlp
import os

# পেজ সেটআপ এবং ব্র্যান্ডিং
st.set_page_config(page_title="Jidan Video Downloader", page_icon="📥", layout="centered")

st.title("📥 Social Media Video Downloader")
st.markdown("Developed by **HABIBULLAH JIDAN**")

# লিঙ্ক ইনপুট বক্স
url = st.text_input("ভিডিও লিঙ্কটি এখানে পেস্ট করুন:", placeholder="https://www.youtube.com/watch?v=...")

if url:
    try:
        # ইউটিউব ডেটা ফেচ করার অপশন
        ydl_opts_info = {
            'quiet': True,
            'no_warnings': True,
            'nocheckcertificate': True,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }

        with yt_dlp.YoutubeDL(ydl_opts_info) as ydl:
            # ভিডিওর ইনফরমেশন বের করা
            info = ydl.extract_info(url, download=False)
            formats = info.get('formats', [])
            title = info.get('title', 'video')
            
            # রেজোলিউশন লিস্ট তৈরি করা (শুধু ভিডিও ফাইলগুলো ফিল্টার করা)
            res_options = {}
            for f in formats:
                if f.get('vcodec') != 'none' and f.get('height'):
                    res = f.get('height')
                    ext = f.get('ext')
                    # সাইজ হিসাব করা (যদি না থাকে তবে ০ দেখাবে)
                    filesize = f.get('filesize') or f.get('filesize_approx') or 0
                    size_mb = f"{filesize/(1024*1024):.1f} MB"
                    
                    label = f"{res}p - {ext} ({size_mb})"
                    res_options[label] = f['format_id']

            # ইউজারকে ড্রপডাউন মেনু দেখানো
            selected_label = st.selectbox("রেজোলিউশন সিলেক্ট করুন:", list(res_options.keys()))

            if st.button("Download Video"):
                st.info("প্রসেসিং হচ্ছে... বড় ভিডিও হলে একটু সময় লাগতে পারে।")
                
                # চূড়ান্ত ডাউনলোড অপশন (Headers সহ)
                out_filename = "final_video.mp4"
                ydl_opts_final = {
                    'format': f"{res_options[selected_label]}+bestaudio/best",
                    'outtmpl': out_filename,
                    'merge_output_format': 'mp4',
                    'nocheckcertificate': True,
                    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                }

                with yt_dlp.YoutubeDL(ydl_opts_final) as ydl:
                    ydl.download([url])
                
                # ওয়েবসাইট থেকে ডাউনলোডের জন্য ফাইল রিড করে বাটন দেখানো
                if os.path.exists(out_filename):
                    with open(out_filename, "rb") as file:
                        st.success("প্রসেসিং সফল হয়েছে!")
                        st.download_button(
                            label="ফাইলটি ডিভাইসে সেভ করতে এখানে ক্লিক করুন",
                            data=file,
                            file_name=f"{title}.mp4",
                            mime="video/mp4"
                        )
                    # ডাউনলোড শেষে সার্ভার থেকে টেম্পোরারি ফাইলটি ডিলিট করা
                    os.remove(out_filename)

    except Exception as e:
        st.error(f"দুঃখিত, একটি সমস্যা হয়েছে: {str(e)}")

# কন্টাক্ট সেকশন
st.markdown("---")
st.markdown(f"© 2026 **HABIBULLAH JIDAN** | [Contact on Facebook](https://www.facebook.com/profile.php?id=100087711907484)")

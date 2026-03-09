import os
import copy

TAR_ACCENT = "AmericanMidwest"
MODE = "content" # "content" or "content-style"
TAR_IDX = [2, 3]

MODELS = {
    "source": "Accent-DSRT/audios/gt_16k",
    "target": "Accent-DSRT/audios/gt_16k",
}
if MODE == "content":
    MODELS.update({
        "vevo": "Accent-DSRT/audios/vevo-content",
        "proposed": "Accent-DSRT/audios/proposed-content",
    })
elif MODE == "content-style":
    MODELS.update({
        "vevo": "Accent-DSRT/audios/vevo-content-style",
        "proposed": "Accent-DSRT/audios/proposed-content-style",
    })

ACC_SPKS = {
    "SouthernEnglish": [
       "p225", "p226", "p228", "p232"
    ],
    "AmericanMidwest":[
       "p311", "p333", "p334", "p341"
    ],
    "Oceanian": [
       "p326", "p335", "p374"
    ],
    "Scottish": [
        "p264", "p265", "p284", "p285"
    ],
}

TEMPLATE_PATH = "template.html"
def read_template(path):
    with open(path, "r") as f:
        template = f.read()
    return template
TEMPLATE=read_template(TEMPLATE_PATH)

all_html = []
for idx in TAR_IDX:
    for src_spk in ACC_SPKS[TAR_ACCENT]:
        for tar_spk in ACC_SPKS["SouthernEnglish"]:
            template = copy.deepcopy(TEMPLATE)
            audio_path_1, audio_path_2, audio_path_3, audio_path_4 = None, None, None, None
            
            for model, path in MODELS.items():
                if model in ["source"]:
                    audio_path_1 = os.path.join(path, src_spk, f"{src_spk}_{idx:03d}_mic1.flac")
                    audio_path = audio_path_1
                elif model in ["target"]:
                    audio_path_2 = os.path.join(path, tar_spk, f"{tar_spk}_{idx:03d}_mic1.flac")
                    audio_path = audio_path_2
                elif model in ["vevo"]:
                    audio_path_3 = os.path.join(path, f"{TAR_ACCENT}_test", f"{src_spk}_{idx:03d}_mic1_{tar_spk}.wav")
                    audio_path = audio_path_3
                elif model in ["proposed"]:
                    audio_path_4 = os.path.join(path, f"{TAR_ACCENT}_test", f"{src_spk}_{idx:03d}_mic1_{tar_spk}.wav")
                    audio_path = audio_path_4
                if not os.path.exists(os.path.join("/Users/s2526235/Desktop/research/CV/jzmzhong.github.io", audio_path)):
                    print(f"Audio file {audio_path} does not exist. Skipping.")
                    continue
                
            html_snippet = template.replace("xxx", model).replace("yyy", f"{src_spk} to {tar_spk}, utterance {idx:03d}")
            html_snippet = html_snippet.replace("zzz_1", audio_path_1)
            html_snippet = html_snippet.replace("zzz_1", audio_path_1)
            html_snippet = html_snippet.replace("zzz_2", audio_path_2)
            html_snippet = html_snippet.replace("zzz_3", audio_path_3)
            html_snippet = html_snippet.replace("zzz_4", audio_path_4)
            all_html.append(html_snippet)

with open("generated_audios.html", "w") as f:
    f.write("\n".join(all_html))


    
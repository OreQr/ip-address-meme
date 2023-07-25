from moviepy.editor import (
    TextClip,
    VideoFileClip,
    ImageClip,
    concatenate_videoclips,
    CompositeVideoClip,
)


def formatISP(asn):
    words = asn.split(" ", 1)
    return " ".join(words[1:])


def animate_text(lines, delay, duration):
    clips = []

    for i in enumerate(lines):
        text_lines = []

        for y in range(i[0] + 1):
            text_lines.append(lines[y])

        clip = TextClip(
            "\n".join(text_lines),
            color="white",
            stroke_color="black",
            stroke_width=1,
            size=(500, 500),
            method="caption",
        ).set_duration(delay)
        clips.append(clip)

    total_duration = len(lines) * delay

    clips[-1] = clips[-1].set_duration(duration - total_duration + delay)

    final_clip = concatenate_videoclips(clips)

    return final_clip


def create_video(data):
    lines = [
        f"IP: {data['query']}",
        f"N: {data['lat']}",
        f"E: {data['lon']}",
        f"Country: {data['country']}",
        f"City: {data['city']}",
        f"ZIP: {data['zip']}",
        f"ISP: {formatISP(data['as'])}",
    ]

    fps = 30

    background = VideoFileClip("background.mp4")

    delay = 0.3
    animation = animate_text(lines, delay, background.duration)

    poster = ImageClip("poster.jpg").set_duration(1 / fps)

    final_clip = concatenate_videoclips(
        [
            poster,
            CompositeVideoClip(
                [
                    background,
                    animation.set_position("center"),
                ]
            ),
        ]
    ).set_duration(background.duration)

    final_clip.write_videofile(f"storage/{data['id']}.mp4", fps=fps, logger=None)

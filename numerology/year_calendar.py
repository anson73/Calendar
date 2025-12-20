import os
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
from typing import Dict

from numerology import numerology

class year_calendar:
    def calendar(self, year: int) -> pd.DataFrame:
        txt_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"calendar-{year}.txt")
        image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"calendar-{year}.png")

        all_days = pd.date_range(start=f'{year}-01-01', end=f'{year}-12-31', freq='D').date
        df = pd.DataFrame([numerology().get_info(d) for d in all_days])
        lines = []

        df = df[df['year'] == year]
        year_info = df.head(1).iloc[0]
        lines.append(f"{year_info["year"]}->{year_info["year_reduced"]}\n")

        dfs: Dict[int, pd.DataFrame] = {month: df[df['month'] == month]for month in range(1, 13)}
        for month in range(1, 13):
            df = dfs[month]
            month_info = df.head(1).iloc[0]
            lines.append(f"\n{month_info["month"]}->{month_info["reduced_month"]} | {month_info["lp_month_reduced"]}/{month_info["lp_month_full"]} -> {month_info["lp_month"]}\n")

            for index, day_info in df.iterrows():
                lines.append(f"\t{day_info["day_of_year"]}: {day_info["date"]} | {day_info["day"]}->{day_info["reduced_day"]} | {day_info["lp_day_reduced"]}/{day_info["lp_day_full"]} -> {day_info["lp_day"]}\n")

        text = "".join(lines)

        # Save calendar as txt
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(text)

        # Save calendar as png
        image = self.calendar_image(text)
        image.save(image_path, dpi=(300, 300), quality=100)

    def calendar_image(self, text: str) -> Image.Image: 
        '''
        Convert calendar to png image
        '''
        FONT_SIZE = 30
        SCALE = 1
        PADDING = 30 * SCALE
        COLUMN_GAP = 50 * SCALE
        LINE_SPACING = 6 * SCALE
        BG_COLOR = "white"
        TEXT_COLOR = "black"

        # Select font
        try:
            font = ImageFont.truetype("DejaVuSansMono.ttf", FONT_SIZE * SCALE)
        except IOError:
            font = ImageFont.load_default()

        # Normalize tabs
        lines = text.expandtabs(4).splitlines()

        # Group lines into months
        months = []
        current = []
        for line in lines:
            if not line.strip():
                continue
            if not line.startswith(" "):  # new month
                if current:
                    months.append(current)
                current = [line]
            else:
                current.append(line)
        if current:
            months.append(current)

        # Measure text accurately
        dummy = Image.new("RGB", (1, 1))
        draw = ImageDraw.Draw(dummy)

        month_widths = []
        month_heights = []
        month_line_heights = []

        for month in months:
            widths = []
            heights = []
            for line in month:
                bbox = draw.textbbox((0, 0), line, font=font)
                w = bbox[2] - bbox[0]
                h = bbox[3] - bbox[1]
                widths.append(w)
                heights.append(h)

            month_widths.append(max(widths))
            total_height = sum(heights) + LINE_SPACING * (len(heights) - 1)
            month_heights.append(total_height)
            month_line_heights.append(heights)

        # Create image
        img_width = sum(month_widths) + COLUMN_GAP * (len(months) - 1) + PADDING * 2
        img_height = max(month_heights) + PADDING * 2

        img = Image.new("RGB", (img_width, img_height), BG_COLOR)
        draw = ImageDraw.Draw(img)

        # Render months from left to right
        x = PADDING
        for month, widths, heights in zip(months, month_widths, month_line_heights):
            y = PADDING
            for line, h in zip(month, heights):
                draw.text((x, y), line, fill=TEXT_COLOR, font=font)
                y += h + LINE_SPACING
            x += widths + COLUMN_GAP

        return img

if __name__ == "__main__":
    year_calendar().calendar(2026)

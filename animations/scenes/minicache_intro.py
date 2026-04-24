from manim import *


config.background_color = BLACK

INK = "#E7EDF4"
MUTED = "#9AA6B2"
ACCENT = "#79D2FF"
GREEN = "#7DF0C8"
RED = "#FF8B84"
CARD = "#0B0E12"


def box(width, height, stroke=INK, fill=CARD, opacity=1.0):
    return RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.08,
        stroke_color=stroke,
        stroke_width=2,
        fill_color=fill,
        fill_opacity=opacity,
    )


class MiniCacheDepthAxis(Scene):
    def construct(self):
        title = Text("KV cache papers attack different axes", color=INK, font_size=40)
        title.to_edge(UP)

        left_frame = box(4.8, 3.8, stroke=ACCENT)
        right_frame = box(4.8, 3.8, stroke=GREEN)
        frames = VGroup(left_frame, right_frame).arrange(RIGHT, buff=0.5).shift(DOWN * 0.15)

        left_title = Text("token-axis", color=ACCENT, font_size=26).next_to(left_frame, UP, buff=0.18)
        right_title = Text("depth-axis", color=GREEN, font_size=26).next_to(right_frame, UP, buff=0.18)

        token_grid = VGroup()
        for _ in range(5):
            row = VGroup(*[Square(side_length=0.38, stroke_color=ACCENT, fill_color=ACCENT, fill_opacity=0.08) for _ in range(7)])
            row.arrange(RIGHT, buff=0.04)
            token_grid.add(row)
        token_grid.arrange(DOWN, buff=0.06).move_to(left_frame)

        keep = SurroundingRectangle(VGroup(token_grid[0], token_grid[1], token_grid[2]), color=ACCENT, buff=0.08)
        drop = Cross(VGroup(token_grid[3], token_grid[4]), stroke_color=RED, stroke_width=4).scale(1.1)

        layers = VGroup()
        for idx in range(6):
            rect = box(3.4, 0.38, stroke=GREEN, fill=GREEN, opacity=0.1)
            rect.add(Text(f"layer {idx + 1}", color=INK, font_size=18).move_to(rect))
            layers.add(rect)
        layers.arrange(DOWN, buff=0.12).move_to(right_frame)

        merge_a = SurroundingRectangle(VGroup(layers[2], layers[3]), color=GREEN, buff=0.08)
        merge_b = SurroundingRectangle(VGroup(layers[4], layers[5]), color=GREEN, buff=0.08)
        arrow = Arrow(LEFT * 0.9, RIGHT * 0.9, color=GREEN).move_to(right_frame.get_bottom() + UP * 0.38)
        note = Text("MiniCache compresses across depth", color=MUTED, font_size=24).to_edge(DOWN)

        self.play(Write(title))
        self.play(FadeIn(frames), FadeIn(left_title), FadeIn(right_title))
        self.play(LaggedStart(*[FadeIn(row, shift=UP * 0.08) for row in token_grid], lag_ratio=0.08))
        self.play(Create(keep), Create(drop))
        self.play(LaggedStart(*[FadeIn(layer, shift=RIGHT * 0.08) for layer in layers], lag_ratio=0.08))
        self.play(Create(merge_a), Create(merge_b), GrowArrow(arrow))
        self.play(FadeIn(note))
        self.wait(1)


class MiniCacheLayerMerge(Scene):
    def construct(self):
        title = Text("Middle and deep layers may be redundant", color=INK, font_size=40)
        title.to_edge(UP)

        layer_stack = VGroup()
        colors = [ACCENT, ACCENT, GREEN, GREEN, GREEN, GREEN]
        for idx, color in enumerate(colors):
            rect = box(4.4, 0.46, stroke=color, fill=color, opacity=0.12)
            rect.add(Text(f"layer {idx + 1}", color=INK, font_size=18).move_to(rect))
            layer_stack.add(rect)
        layer_stack.arrange(DOWN, buff=0.16).shift(LEFT * 1.7 + DOWN * 0.15)

        similar_a = SurroundingRectangle(VGroup(layer_stack[2], layer_stack[3]), color=GREEN, buff=0.08)
        similar_b = SurroundingRectangle(VGroup(layer_stack[4], layer_stack[5]), color=GREEN, buff=0.08)

        compressed = VGroup()
        for label in ["compressed pair", "compressed pair"]:
            rect = box(2.8, 0.62, stroke=GREEN, fill=GREEN, opacity=0.12)
            rect.add(Text(label, color=INK, font_size=18).move_to(rect))
            compressed.add(rect)
        compressed.arrange(DOWN, buff=0.36).shift(RIGHT * 2.4)

        arrows = VGroup(
            Arrow(similar_a.get_right(), compressed[0].get_left(), color=GREEN, buff=0.2),
            Arrow(similar_b.get_right(), compressed[1].get_left(), color=GREEN, buff=0.2),
        )

        memory_before = Text("memory before", color=MUTED, font_size=20).next_to(layer_stack, DOWN, buff=0.28)
        memory_after = Text("memory after", color=MUTED, font_size=20).next_to(compressed, DOWN, buff=0.28)
        bars_before = VGroup(*[Rectangle(width=0.42, height=0.18, stroke_width=0, fill_color=ACCENT, fill_opacity=1) for _ in range(6)]).arrange(RIGHT, buff=0.06).next_to(memory_before, DOWN, buff=0.16)
        bars_after = VGroup(*[Rectangle(width=0.42, height=0.18, stroke_width=0, fill_color=GREEN, fill_opacity=1) for _ in range(4)]).arrange(RIGHT, buff=0.06).next_to(memory_after, DOWN, buff=0.16)

        note = Text("compress the cache without only dropping tokens", color=MUTED, font_size=24).to_edge(DOWN)

        self.play(Write(title))
        self.play(LaggedStart(*[FadeIn(layer, shift=UP * 0.08) for layer in layer_stack], lag_ratio=0.08))
        self.play(Create(similar_a), Create(similar_b))
        self.play(GrowArrow(arrows[0]), FadeIn(compressed[0]))
        self.play(GrowArrow(arrows[1]), FadeIn(compressed[1]))
        self.play(FadeIn(memory_before), FadeIn(bars_before))
        self.play(FadeIn(memory_after), FadeIn(bars_after))
        self.play(FadeIn(note))
        self.wait(1)


class MiniCacheRetention(Scene):
    def construct(self):
        title = Text("Retention keeps the sharp mismatches", color=INK, font_size=40)
        title.to_edge(UP)

        tokens = VGroup()
        fills = [GREEN, GREEN, GREEN, RED, GREEN, RED, GREEN, GREEN]
        labels = ["0.98", "0.97", "0.99", "0.71", "0.96", "0.68", "0.98", "0.99"]
        for fill, label in zip(fills, labels):
            square = RoundedRectangle(
                width=0.78,
                height=0.78,
                corner_radius=0.08,
                stroke_color=fill,
                stroke_width=2,
                fill_color=fill,
                fill_opacity=0.12,
            )
            number = Text(label, color=INK, font_size=18).move_to(square)
            tokens.add(VGroup(square, number))
        tokens.arrange(RIGHT, buff=0.14).shift(UP * 0.35)

        caption = Text("cross-layer similarity per token", color=MUTED, font_size=24).next_to(tokens, UP, buff=0.24)
        threshold = DashedLine(
            start=tokens.get_left() + DOWN * 0.85,
            end=tokens.get_right() + DOWN * 0.85,
            color=MUTED,
            dash_length=0.1,
        )
        threshold_label = Text("similar enough -> merge", color=GREEN, font_size=22).next_to(threshold, DOWN, buff=0.16)

        kept = VGroup(
            SurroundingRectangle(tokens[3], color=RED, buff=0.08),
            SurroundingRectangle(tokens[5], color=RED, buff=0.08),
        )
        kept_label = Text("retain the unusually distinct pairs", color=RED, font_size=24).to_edge(DOWN)

        self.play(Write(title))
        self.play(FadeIn(caption))
        self.play(LaggedStart(*[FadeIn(token, shift=UP * 0.08) for token in tokens], lag_ratio=0.08))
        self.play(Create(threshold), FadeIn(threshold_label))
        self.play(Create(kept[0]), Create(kept[1]))
        self.play(FadeIn(kept_label))
        self.wait(1)

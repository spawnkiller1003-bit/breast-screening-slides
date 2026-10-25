#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def create_report():
    doc = Document()
    
    # 1. 頁面邊距設定 (A4, 2.5cm)
    section = doc.sections[0]
    section.page_width = Cm(21.0)
    section.page_height = Cm(29.7)
    section.top_margin = Cm(2.2)
    section.bottom_margin = Cm(2.2)
    section.left_margin = Cm(2.2)
    section.right_margin = Cm(2.2)
    
    # 色彩定義 (優雅醫療深藍與質樸灰色調)
    C_PRIMARY_NAVY = RGBColor(26, 54, 93)       # #1A365D - 深曜藍 (大標題、主視覺)
    C_SECONDARY_BLUE = RGBColor(37, 99, 235)    # #2563EB - 科技藍 (次標題、重點)
    C_ACCENT_TEAL = RGBColor(13, 148, 136)      # #0D9488 - 臨床綠 (亮點、洞察)
    C_ACCENT_ROSE = RGBColor(190, 18, 60)       # #BE123C - 警戒玫瑰紅 (警訊、重要名次)
    C_TEXT_DARK = RGBColor(31, 41, 55)          # #1F2937 - 內文主深灰
    C_TEXT_MUTED = RGBColor(100, 116, 139)      # #64748B - 次要輔助文字
    
    HEX_PRIMARY_NAVY = "1A365D"
    HEX_LIGHT_BLUE = "F0F4F8"
    HEX_ALT_ROW = "F8FAFC"
    HEX_LIGHT_GREEN = "F0FDF4"
    HEX_BORDER = "CBD5E1"
    HEX_TEAL_BORDER = "0D9488"
    HEX_BLUE_BORDER = "2563EB"
    
    FONT_CHINESE = "微軟正黑體"
    FONT_ENGLISH = "Arial"
    
    # 輔助函式：文字樣式套用
    def format_run(run, font_name=FONT_CHINESE, size_pt=10.5, bold=False, italic=False, color_rgb=C_TEXT_DARK):
        run.font.name = font_name
        run.font.size = Pt(size_pt)
        run.bold = bold
        run.italic = italic
        run.font.color.rgb = color_rgb
        rPr = run._r.get_or_add_rPr()
        rFonts = parse_xml(f'<w:rFonts {nsdecls("w")} w:ascii="{FONT_ENGLISH}" w:hAnsi="{FONT_ENGLISH}" w:eastAsia="{font_name}" w:cs="{FONT_ENGLISH}"/>')
        rPr.append(rFonts)

    def set_cell_margins(cell, top=140, bottom=140, left=180, right=180):
        tcPr = cell._tc.get_or_add_tcPr()
        tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
        tcPr.append(tcMar)

    def set_cell_shading(cell, color_hex):
        shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
        cell._tc.get_or_add_tcPr().append(shd)

    def set_table_styling(table, col_widths, border_color=HEX_BORDER):
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        tblPr = table._tbl.tblPr
        tblBorders = parse_xml(f'''
            <w:tblBorders {nsdecls("w")}>
                <w:top w:val="single" w:sz="6" w:space="0" w:color="{border_color}"/>
                <w:left w:val="none"/>
                <w:bottom w:val="single" w:sz="8" w:space="0" w:color="{HEX_PRIMARY_NAVY}"/>
                <w:right w:val="none"/>
                <w:insideH w:val="single" w:sz="4" w:space="0" w:color="{border_color}"/>
                <w:insideV w:val="none"/>
            </w:tblBorders>
        ''')
        tblPr.append(tblBorders)
        
        # 設定寬度與防跨頁斷裂
        for row in table.rows:
            trPr = row._tr.get_or_add_trPr()
            trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
            for idx, width in enumerate(col_widths):
                if idx < len(row.cells):
                    row.cells[idx].width = Cm(width)
                    set_cell_margins(row.cells[idx])
        # 重複標頭
        header_trPr = table.rows[0]._tr.get_or_add_trPr()
        header_trPr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))

    def add_callout(text, title="分析摘要", border_color=HEX_TEAL_BORDER, bg_color=HEX_LIGHT_GREEN):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.cell(0, 0)
        cell.width = Cm(16.6)
        tcPr = cell._tc.get_or_add_tcPr()
        shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{bg_color}"/>')
        tcBorders = parse_xml(f'''
            <w:tcBorders {nsdecls("w")}>
                <w:top w:val="none"/>
                <w:left w:val="single" w:sz="24" w:space="0" w:color="{border_color}"/>
                <w:bottom w:val="none"/>
                <w:right w:val="none"/>
            </w:tcBorders>
        ''')
        tcPr.append(shd)
        tcPr.append(tcBorders)
        set_cell_margins(cell, top=160, bottom=160, left=240, right=200)
        
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.25
        run_title = p.add_run(f"💡 {title}\n")
        format_run(run_title, size_pt=10.5, bold=True, color_rgb=C_PRIMARY_NAVY)
        run_text = p.add_run(text)
        format_run(run_text, size_pt=10.0, color_rgb=C_TEXT_DARK)
        
        doc.add_paragraph().paragraph_format.space_after = Pt(4)

    # 頁首與頁尾
    header = section.header
    hp = header.paragraphs[0]
    hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    hrun = hp.add_run("守護乳房健康講座 — 成效檢討與未來場次籌備報告 (PAR Report)")
    format_run(hrun, size_pt=8.5, color_rgb=C_TEXT_MUTED)
    
    footer = section.footer
    fp = footer.paragraphs[0]
    fp.alignment = WD_ALIGN_PARAGRAPH.LEFT
    frun1 = fp.add_run("敏盛綜合醫院巡檢團隊 · 國軍桃園總醫院乳房外科 梁祖瑋醫師  |  受邀單位：瑞健醫療 (SHL Medical)")
    format_run(frun1, size_pt=8.5, color_rgb=C_TEXT_MUTED)

    # ------------------ 文件主標題與副標題 ------------------
    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(8)
    p_title.paragraph_format.space_after = Pt(2)
    p_title.paragraph_format.line_spacing = 1.15
    run_main_title = p_title.add_run("乳癌篩檢衛教講座成效檢討與未來場次籌備報告")
    format_run(run_main_title, size_pt=21.0, bold=True, color_rgb=C_PRIMARY_NAVY)
    
    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_after = Pt(14)
    run_sub = p_sub.add_run("Post-Action Review (PAR) Report & Operational SOP for Breast Cancer Screening Lectures")
    format_run(run_sub, size_pt=10.0, italic=True, color_rgb=C_TEXT_MUTED)

    # ------------------ 基本資訊卡片表格 ------------------
    meta_table = doc.add_table(rows=6, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_data = [
        ("講座主題", "守護乳房健康 — 科技業女性乳癌預防與篩檢實務"),
        ("主講醫師", "梁祖瑋 醫師（敏盛綜合醫院巡檢醫師／國軍桃園總醫院乳房外科）"),
        ("受邀單位", "瑞健醫療（SHL Medical）"),
        ("實施場次", "第一場：桃園廠（115/10/07） | 第二場：南崁廠（115/10/14） | 第三場：六福廠（115/10/21）"),
        ("問卷來源", "Google Forms 線上現場問卷（課後即時掃碼填答，有效樣本 N = 33 份完全有效問卷）"),
        ("報告目的", "檢視三場次之量化數據與質性回饋，建立日後各級企業、機關與院所巡檢衛教之標準化作業模組（SOP）與內容迭代依據。")
    ]
    set_table_styling(meta_table, [3.8, 12.8], border_color="E2E8F0")
    for idx, (label, val) in enumerate(meta_data):
        row = meta_table.rows[idx]
        set_cell_shading(row.cells[0], "F1F5F9")
        set_cell_shading(row.cells[1], "FFFFFF" if idx % 2 == 0 else "F8FAFC")
        
        p0 = row.cells[0].paragraphs[0]
        p0.paragraph_format.space_after = Pt(0)
        p0.paragraph_format.line_spacing = 1.2
        r0 = p0.add_run(label)
        format_run(r0, size_pt=10.0, bold=True, color_rgb=C_PRIMARY_NAVY)
        
        p1 = row.cells[1].paragraphs[0]
        p1.paragraph_format.space_after = Pt(0)
        p1.paragraph_format.line_spacing = 1.2
        r1 = p1.add_run(val)
        format_run(r1, size_pt=10.0, color_rgb=C_TEXT_DARK)

    p_spacer = doc.add_paragraph()
    p_spacer.paragraph_format.space_after = Pt(8)

    # ------------------ 原始問卷表單設計規範 ------------------
    h1 = doc.add_paragraph()
    h1.paragraph_format.space_before = Pt(14)
    h1.paragraph_format.space_after = Pt(6)
    r_h1 = h1.add_run("原始問卷表單設計規範 (Questionnaire Instrument)")
    format_run(r_h1, size_pt=15.0, bold=True, color_rgb=C_PRIMARY_NAVY)
    
    p_desc = doc.add_paragraph()
    p_desc.paragraph_format.space_after = Pt(6)
    r_desc = p_desc.add_run("本次巡迴講座採用統一之 Google 表單進行即時滿意度與行為意向調查，題項架構如下，做為後續各專場一致性評量基準：")
    format_run(r_desc, size_pt=10.0, color_rgb=C_TEXT_MUTED)

    # 問卷題目方框容器
    q_box = doc.add_table(rows=1, cols=1)
    q_box.alignment = WD_TABLE_ALIGNMENT.CENTER
    q_cell = q_box.cell(0, 0)
    q_cell.width = Cm(16.6)
    tcPr = q_cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="F8FAFC"/>')
    tcBorders = parse_xml(f'''
        <w:tcBorders {nsdecls("w")}>
            <w:top w:val="single" w:sz="4" w:space="0" w:color="{HEX_BORDER}"/>
            <w:left w:val="single" w:sz="18" w:space="0" w:color="{HEX_PRIMARY_NAVY}"/>
            <w:bottom w:val="single" w:sz="4" w:space="0" w:color="{HEX_BORDER}"/>
            <w:right w:val="single" w:sz="4" w:space="0" w:color="{HEX_BORDER}"/>
        </w:tcBorders>
    ''')
    tcPr.append(shd)
    tcPr.append(tcBorders)
    set_cell_margins(q_cell, top=160, bottom=160, left=220, right=200)
    
    qp = q_cell.paragraphs[0]
    qp.paragraph_format.space_after = Pt(3)
    qp.paragraph_format.line_spacing = 1.25
    r_qtitle = qp.add_run("表單名稱：守護乳房健康講座 — 現場回饋問卷\n")
    format_run(r_qtitle, size_pt=11.0, bold=True, color_rgb=C_PRIMARY_NAVY)
    r_qintro = qp.add_run("前言說明：感謝您參與梁祖瑋醫師主講的「守護乳房健康講座」。本問卷僅需 1 分鐘填寫，您的寶貴意見將是我們持續推動職場健康守護的最大動力！\n\n")
    format_run(r_qintro, size_pt=9.5, italic=True, color_rgb=C_TEXT_MUTED)
    
    questions_text = [
        ("Q1. 透過本次講座，您對 114 年起國家最新公費篩檢新制的掌握程度為何？【單選，必填】", [
            "完全清楚！我知道 114 年起 40～74 歲全民全面享有每 2 年一次公費乳房攝影，不論有無家族史皆補助",
            "很清楚！我知道未滿 40 歲若有一/二等親家族史等高風險因子，建議自 30 歲起定期進行乳房超音波檢查",
            "清楚！我知道早期篩檢能發現無症狀微小鈣化點，把握 40 歲黃金受檢時機",
            "大致了解，演講後會主動查詢自己與家人的篩檢院所資訊"
        ]),
        ("Q2. 今天 24 關簡報中，哪一個主題或數據讓您印象最深刻？【複選最多 3 項，必填】", [
            "壞習慣健康價標動態計算機（全糖手搖飲、久坐、熬夜的體內發炎試算）",
            "5 大生活防禦指南（地中海抗發炎微替換餐盤、每週 150 分鐘微運動）",
            "篩檢資格即時判定工具（快速釐清自己與家人的受檢年齡與福利）",
            "戳破 5 大檢查迷思（減痛三秘訣、單次輻射僅如台北舊金山飛行、洗澡摸硬塊盲點）",
            "BI-RADS 報告分級解碼（Category 0 不是第 0 期癌，只是需補做超音波）",
            "檢查工具地圖與派工羅盤（超音波與攝影的戰場與盲區互補、加做檢查羅盤）",
            "七大乳房異常警訊鑑別（無痛硬塊、局部凹陷、單側血水、淋巴腫大等良惡性鑑別）",
            "存活率階梯剖析（第 0~1 期高達 95~99.9% 治癒率 vs 晚期劇降，早期發現是關鍵）"
        ]),
        ("Q3. 接下來 3～6 個月內，您的具體健康行動計劃是？【單選，必填】", [
            "我會先從改善日常生活習慣（減糖、增加活動量、規律作息）開始做起",
            "我會主動提醒並協助身邊符合資格的家人（母親、太太、姊妹、同事）去受檢",
            "我符合資格，近期會主動預約公費乳房 X 光攝影",
            "我未滿 40 歲，但會為自己預約一次乳房超音波基礎檢查",
            "目前暫無規劃"
        ]),
        ("Q4. 您對梁祖瑋醫師的授課風格與專業呈現感受為何？【單選，必填】", [
            "深入淺出，用科技與數據思維解說醫學，生動好懂、完全不沉悶！",
            "態度親切專業，提供具體清晰的行動指南，讓人很有安心感",
            "節奏明快、架構極有邏輯，打破傳統衛教說教的刻板印象",
            "內容相當扎實豐富，希望未來還有進階主題分享"
        ]),
        ("Q5. 本次講座採用「網頁互動儀表板式投影片」呈現，您的體驗感受為？【單選，必填】", [
            "非常驚艷！比傳統 PPT 更有現代感、科技感與即時互動性",
            "掃碼即可在手機上完整帶走整份簡報，非常實用方便！",
            "字體大且對比清晰，即使坐在會議室後排也能輕鬆看清",
            "與一般簡報差不多"
        ]),
        ("Q6. 您還有任何想請教梁醫師的問題，或是想對梁醫師說的鼓勵與建議嗎？【開放問答，選填】", [
            "[ 文字自由輸入框 ]"
        ])
    ]
    
    for q_idx, (q_header, opts) in enumerate(questions_text):
        r_qh = qp.add_run(f"\n{q_header}\n")
        format_run(r_qh, size_pt=9.5, bold=True, color_rgb=C_PRIMARY_NAVY)
        for opt in opts:
            box_prefix = "  ☐ " if "[" not in opt else "  "
            r_opt = qp.add_run(f"{box_prefix}{opt}\n")
            format_run(r_opt, size_pt=9.0, color_rgb=C_TEXT_DARK)

    p_spacer2 = doc.add_paragraph()
    p_spacer2.paragraph_format.space_after = Pt(10)

    # ------------------ 第一部分：定量數據深度剖析 ------------------
    h1_p1 = doc.add_paragraph()
    h1_p1.paragraph_format.space_before = Pt(16)
    h1_p1.paragraph_format.space_after = Pt(6)
    r_h1_p1 = h1_p1.add_run("第一部分：問卷定量統計與受眾行為分析 (Quantitative Findings)")
    format_run(r_h1_p1, size_pt=15.0, bold=True, color_rgb=C_PRIMARY_NAVY)

    # --- Q1 ---
    h2_q1 = doc.add_paragraph()
    h2_q1.paragraph_format.space_before = Pt(8)
    h2_q1.paragraph_format.space_after = Pt(4)
    r_h2_q1 = h2_q1.add_run("一、國家最新公費篩檢新制掌握程度（Q1）")
    format_run(r_h2_q1, size_pt=12.0, bold=True, color_rgb=C_SECONDARY_BLUE)
    
    p_q1_note = doc.add_paragraph()
    p_q1_note.paragraph_format.space_after = Pt(4)
    r_q1_note = p_q1_note.add_run("114 年起衛生福利部正式將公費乳房 X 光攝影擴大為 40～74 歲婦女（每 2 年 1 次），本題評估聽眾對重大衛政變革之吸收成效（單選，N = 33）：")
    format_run(r_q1_note, size_pt=10.0, color_rgb=C_TEXT_MUTED)
    
    t_q1 = doc.add_table(rows=6, cols=3)
    set_table_styling(t_q1, [11.2, 2.6, 2.8])
    t_q1_headers = ["選項內容", "填答人數", "百分比"]
    for i, h in enumerate(t_q1_headers):
        cell = t_q1.rows[0].cells[i]
        set_cell_shading(cell, HEX_PRIMARY_NAVY)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER if i > 0 else WD_ALIGN_PARAGRAPH.LEFT
        r = p.add_run(h)
        format_run(r, size_pt=10.0, bold=True, color_rgb=RGBColor(255, 255, 255))
        
    t_q1_data = [
        ("完全清楚！40～74 歲全面享有每 2 年一次公費乳房攝影，無家族史亦補助", "26", "78.8%"),
        ("很清楚！未滿 40 歲若有一/二等親家族史等高風險因子，建議 30 歲起定期超音波", "3", "9.1%"),
        ("清楚！早期篩檢能發現無症狀微小鈣化點，把握 40 歲黃金受檢時機", "1", "3.0%"),
        ("大致了解，演講後會主動查詢自己與家人的篩檢院所資訊", "3", "9.1%"),
        ("合計", "33", "100.0%")
    ]
    for row_idx, data in enumerate(t_q1_data, start=1):
        row = t_q1.rows[row_idx]
        is_total = (row_idx == len(t_q1_data))
        bg = HEX_LIGHT_BLUE if is_total else (HEX_ALT_ROW if row_idx % 2 == 0 else "FFFFFF")
        for col_idx, text in enumerate(data):
            cell = row.cells[col_idx]
            set_cell_shading(cell, bg)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if col_idx > 0 else WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(text)
            format_run(r, size_pt=9.5, bold=is_total, color_rgb=C_PRIMARY_NAVY if is_total else C_TEXT_DARK)
            
    add_callout(
        "90.9% 的聽眾展現高度掌握度，其中近八成（78.8%）能明確複述「40～74 歲免家族史全面公費」之關鍵政策。透過第 10 關的「公費資格判定卡」即時互動，極有效掃除坊間普遍停留於「45 歲才開始補助」之舊資訊斷層。",
        title="政策掌握度深度洞察"
    )

    # --- Q2 ---
    h2_q2 = doc.add_paragraph()
    h2_q2.paragraph_format.space_before = Pt(8)
    h2_q2.paragraph_format.space_after = Pt(4)
    r_h2_q2 = h2_q2.add_run("二、今天 24 關簡報中哪一個主題讓您印象最深刻？（Q2 模組共鳴度）")
    format_run(r_h2_q2, size_pt=12.0, bold=True, color_rgb=C_SECONDARY_BLUE)
    
    p_q2_note = doc.add_paragraph()
    p_q2_note.paragraph_format.space_after = Pt(4)
    r_q2_note = p_q2_note.add_run("本題為複選題（每人最多 3 項，共計有效勾選 86 次），評估各衛教模組在受眾心中的記憶點與說服力：")
    format_run(r_q2_note, size_pt=10.0, color_rgb=C_TEXT_MUTED)
    
    t_q2 = doc.add_table(rows=9, cols=5)
    set_table_styling(t_q2, [1.4, 6.6, 2.0, 2.2, 4.4])
    t_q2_headers = ["排序", "模組主題單元", "得票數", "得票率", "受眾認知驅動因素剖析"]
    for i, h in enumerate(t_q2_headers):
        cell = t_q2.rows[0].cells[i]
        set_cell_shading(cell, HEX_PRIMARY_NAVY)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER if i in [0, 2, 3] else WD_ALIGN_PARAGRAPH.LEFT
        r = p.add_run(h)
        format_run(r, size_pt=10.0, bold=True, color_rgb=RGBColor(255, 255, 255))
        
    t_q2_data = [
        ("1 🥇", "壞習慣健康價標動態計算機", "19 票", "57.6%", "共鳴度冠軍。科技業講求量化指標，將手搖飲、久坐、熬夜換算為發炎價標，直擊高壓工作常態。"),
        ("2 🥈", "七大乳房異常警訊鑑別", "15 票", "45.5%", "「無痛腫塊才是最危險硬塊」與局部凹陷，解開女性長年自我檢查摸硬塊之誤區。"),
        ("3 🥉", "BI-RADS 報告分級解碼", "13 票", "39.4%", "解開健康檢查報告的焦慮，釐清「Category 0 代表需補做超音波，非第 0 期癌」。"),
        ("3 🥉", "存活率階梯剖析", "13 票", "39.4%", "第 0~1 期 95~99.9% vs 晚期劇降之階梯震撼，強化早篩早治的理性驅動力。"),
        ("5", "5 大生活防禦指南", "8 票", "24.2%", "雙色花椰菜炒黑木耳替換原則與 150 分鐘微運動，屬易於執行的生活指引。"),
        ("5", "檢查工具地圖與派工羅盤", "8 票", "24.2%", "超音波（緻密腺體）與攝影（微小鈣化點）之臨床戰場與盲區互補分工。"),
        ("7", "篩檢資格即時判定工具", "5 票", "15.2%", "協助快速自評自己與家屬之公費受檢年齡與福利。"),
        ("8", "戳破 5 大檢查迷思", "4 票", "12.1%", "減痛三要訣與「單次攝影輻射等同台北舊金山往返飛行一次」之等價換算。")
    ]
    for row_idx, data in enumerate(t_q2_data, start=1):
        row = t_q2.rows[row_idx]
        bg = HEX_ALT_ROW if row_idx % 2 == 0 else "FFFFFF"
        if row_idx == 1:
            bg = "FEF2F2"  # 首選淡粉紅強調
        for col_idx, text in enumerate(data):
            cell = row.cells[col_idx]
            set_cell_shading(cell, bg)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if col_idx in [0, 2, 3] else WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(text)
            is_bold = col_idx in [0, 1] and row_idx <= 4
            color = C_ACCENT_ROSE if (row_idx == 1 and col_idx in [0, 1]) else C_TEXT_DARK
            format_run(r, size_pt=9.0, bold=is_bold, color_rgb=color)

    add_callout(
        "科技業聽眾對「數據視覺化（壞習慣發炎計算機 57.6%）」與「邏輯決策樹（七大警訊鑑別 45.5%、BI-RADS 解碼 39.4%）」展現出極高的共鳴黏著度。未來的講座應確保此三大模組維持為黃金保留核心。",
        title="課程模組共鳴度洞察"
    )

    # --- Q3 ---
    h2_q3 = doc.add_paragraph()
    h2_q3.paragraph_format.space_before = Pt(8)
    h2_q3.paragraph_format.space_after = Pt(4)
    r_h2_q3 = h2_q3.add_run("三、課後 3～6 個月內具體健康行動計劃（Q3 行動意向）")
    format_run(r_h2_q3, size_pt=12.0, bold=True, color_rgb=C_SECONDARY_BLUE)
    
    t_q3 = doc.add_table(rows=7, cols=4)
    set_table_styling(t_q3, [3.4, 8.8, 2.2, 2.2])
    t_q3_headers = ["行動層次類別", "具體行動計劃內容", "人數", "百分比"]
    for i, h in enumerate(t_q3_headers):
        cell = t_q3.rows[0].cells[i]
        set_cell_shading(cell, HEX_PRIMARY_NAVY)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER if i in [0, 2, 3] else WD_ALIGN_PARAGRAPH.LEFT
        r = p.add_run(h)
        format_run(r, size_pt=10.0, bold=True, color_rgb=RGBColor(255, 255, 255))
        
    t_q3_data = [
        ("生活習慣改善", "我會先從改善日常生活習慣（減糖、增加活動量、規律作息）開始做起", "19", "57.6%"),
        ("利他推廣行動", "我會主動提醒並協助身邊符合資格的家人（母親、太太、姊妹、同事）受檢", "7", "21.2%"),
        ("直接受檢行動", "我符合資格，近期會主動預約公費乳房 X 光攝影", "4", "12.1%"),
        ("自主預防檢查", "我未滿 40 歲，但會為自己預約一次乳房超音波基礎檢查", "3", "9.1%"),
        ("消極觀望", "目前暫無規劃", "0", "0.0%"),
        ("合計", "", "33", "100.0%")
    ]
    for row_idx, data in enumerate(t_q3_data, start=1):
        row = t_q3.rows[row_idx]
        is_total = (row_idx == len(t_q3_data))
        bg = HEX_LIGHT_BLUE if is_total else (HEX_ALT_ROW if row_idx % 2 == 0 else "FFFFFF")
        for col_idx, text in enumerate(data):
            cell = row.cells[col_idx]
            set_cell_shading(cell, bg)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if col_idx in [0, 2, 3] else WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(text)
            format_run(r, size_pt=9.5, bold=is_total, color_rgb=C_PRIMARY_NAVY if is_total else C_TEXT_DARK)

    add_callout(
        "1. 達成「零觀望」：0 人選擇目前暫無規劃，全體聽眾（100%）在聽講後皆具備實質健康作為意向。\n2. 雙軌乘數效應：除了自我預約受檢（21.2%）與生活作息改善（57.6%）外，高達 21.2% 的同仁承諾向外推廣協助家人受檢，展現極強的健康大使外溢效應。",
        title="行動轉化結構分析"
    )

    # --- Q4 & Q5 (雙表格並列或緊湊排列) ---
    h2_q4 = doc.add_paragraph()
    h2_q4.paragraph_format.space_before = Pt(8)
    h2_q4.paragraph_format.space_after = Pt(4)
    r_h2_q4 = h2_q4.add_run("四、梁醫師授課風格與投影片體驗評價（Q4 & Q5）")
    format_run(r_h2_q4, size_pt=12.0, bold=True, color_rgb=C_SECONDARY_BLUE)

    t_q4 = doc.add_table(rows=6, cols=3)
    set_table_styling(t_q4, [11.2, 2.6, 2.8])
    for i, h in enumerate(["Q4 梁醫師授課風格與專業呈現感受", "人數", "百分比"]):
        cell = t_q4.rows[0].cells[i]
        set_cell_shading(cell, HEX_PRIMARY_NAVY)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER if i > 0 else WD_ALIGN_PARAGRAPH.LEFT
        r = p.add_run(h)
        format_run(r, size_pt=9.5, bold=True, color_rgb=RGBColor(255, 255, 255))
        
    t_q4_data = [
        ("深入淺出，用科技與數據思維解說醫學，生動好懂、完全不沉悶！", "15", "45.5%"),
        ("態度親切專業，提供具體清晰的行動指南，讓人很有安心感", "13", "39.4%"),
        ("節奏明快、架構極有邏輯，打破傳統衛教說教的刻板印象", "3", "9.1%"),
        ("內容相當扎實豐富，希望未來還有進階主題分享", "2", "6.1%"),
        ("合計", "33", "100.0%")
    ]
    for row_idx, data in enumerate(t_q4_data, start=1):
        row = t_q4.rows[row_idx]
        is_total = (row_idx == len(t_q4_data))
        bg = HEX_LIGHT_BLUE if is_total else (HEX_ALT_ROW if row_idx % 2 == 0 else "FFFFFF")
        for col_idx, text in enumerate(data):
            cell = row.cells[col_idx]
            set_cell_shading(cell, bg)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if col_idx > 0 else WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(text)
            format_run(r, size_pt=9.0, bold=is_total, color_rgb=C_PRIMARY_NAVY if is_total else C_TEXT_DARK)

    doc.add_paragraph().paragraph_format.space_after = Pt(2)

    t_q5 = doc.add_table(rows=6, cols=3)
    set_table_styling(t_q5, [11.2, 2.6, 2.8])
    for i, h in enumerate(["Q5 網頁互動儀表板式投影片體驗感受", "人數", "百分比"]):
        cell = t_q5.rows[0].cells[i]
        set_cell_shading(cell, HEX_PRIMARY_NAVY)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER if i > 0 else WD_ALIGN_PARAGRAPH.LEFT
        r = p.add_run(h)
        format_run(r, size_pt=9.5, bold=True, color_rgb=RGBColor(255, 255, 255))
        
    t_q5_data = [
        ("非常驚艷！比傳統 PPT 更有現代感、科技感與即時互動性", "18", "54.5%"),
        ("掃碼即可在手機上完整帶走整份簡報，非常實用方便！", "10", "30.3%"),
        ("字體大且對比清晰，即使坐在會議室後排也能輕鬆看清", "4", "12.1%"),
        ("與一般簡報差不多", "1", "3.0%"),
        ("合計", "33", "100.0%")
    ]
    for row_idx, data in enumerate(t_q5_data, start=1):
        row = t_q5.rows[row_idx]
        is_total = (row_idx == len(t_q5_data))
        bg = HEX_LIGHT_BLUE if is_total else (HEX_ALT_ROW if row_idx % 2 == 0 else "FFFFFF")
        for col_idx, text in enumerate(data):
            cell = row.cells[col_idx]
            set_cell_shading(cell, bg)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if col_idx > 0 else WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(text)
            format_run(r, size_pt=9.0, bold=is_total, color_rgb=C_PRIMARY_NAVY if is_total else C_TEXT_DARK)

    p_spacer3 = doc.add_paragraph()
    p_spacer3.paragraph_format.space_after = Pt(10)

    # ------------------ 第二部分：聽眾質性意見與反饋分類 ------------------
    h1_p2 = doc.add_paragraph()
    h1_p2.paragraph_format.space_before = Pt(16)
    h1_p2.paragraph_format.space_after = Pt(6)
    r_h1_p2 = h1_p2.add_run("第二部分：聽眾開放式質性意見與反饋分類 (Qualitative Analysis)")
    format_run(r_h1_p2, size_pt=15.0, bold=True, color_rgb=C_PRIMARY_NAVY)

    p_p2_intro = doc.add_paragraph()
    p_p2_intro.paragraph_format.space_after = Pt(6)
    r_p2_intro = p_p2_intro.add_run("Q6 為開放選填問答，共計回收 18 則回應（排除無、NA 等無效回覆後，實質文本為 15 則）。經質性編碼歸類為四大主軸，原音記錄如下：")
    format_run(r_p2_intro, size_pt=10.0, color_rgb=C_TEXT_MUTED)

    feedback_groups = [
        ("類別 A：講師台風與授課技巧肯定 (6 則)", [
            "醫生聲音溫柔 仔細講解 內容清楚好懂 謝謝梁醫生",
            "謝謝醫師的專業分享、幽默風趣的解說方式讓人會更有興趣聽講。",
            "演講風格很輕鬆明快",
            "講解淺而易懂",
            "內容簡單明瞭，謝謝梁醫生的細心講解！",
            "醫師衛教很有趣"
        ], "F0FDF4", "0D9488"),
        ("類別 B：專業知識與實用價值反饋 (6 則)", [
            "梁醫師的講座十分精彩，學習到很多專業知識跟常規保健方法",
            "很實用的內容，印象深刻",
            "內容充實清楚",
            "很清楚 超讚",
            "很清楚",
            "謝謝醫師和 SHL"
        ], "EFF6FF", "2563EB"),
        ("類別 C：場地視覺與技術體驗反饋 (1 則)", [
            "網頁互動儀表板式投影片很特別,但字太小了,做比較遠會看不清楚\n【備註】：來自首場桃園廠，已作為第二、三場全面重構大字滿版之核心依據。"
        ], "FEF2F2", "BE123C"),
        ("類別 D：課程內容延伸建議 (1 則)", [
            "謝謝醫師精彩的演講與對乳癌相關詳細的介紹，或許可以增加幾個案例說明，譬如安潔莉娜裘莉。\n【備註】：聽眾渴望知名人物案例，以深層理解 BRCA 基因突變、家族史風險與預防性切除之抉擇思維。"
        ], "FFFBEB", "D97706")
    ]

    for g_title, g_items, g_bg, g_border in feedback_groups:
        h3_g = doc.add_paragraph()
        h3_g.paragraph_format.space_before = Pt(8)
        h3_g.paragraph_format.space_after = Pt(3)
        r_gh = h3_g.add_run(g_title)
        format_run(r_gh, size_pt=11.0, bold=True, color_rgb=C_PRIMARY_NAVY)
        
        fb_tbl = doc.add_table(rows=1, cols=1)
        fb_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        fb_cell = fb_tbl.cell(0, 0)
        fb_cell.width = Cm(16.6)
        tcPr = fb_cell._tc.get_or_add_tcPr()
        shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{g_bg}"/>')
        tcBorders = parse_xml(f'''
            <w:tcBorders {nsdecls("w")}>
                <w:top w:val="none"/>
                <w:left w:val="single" w:sz="20" w:space="0" w:color="{g_border}"/>
                <w:bottom w:val="none"/>
                <w:right w:val="none"/>
            </w:tcBorders>
        ''')
        tcPr.append(shd)
        tcPr.append(tcBorders)
        set_cell_margins(fb_cell, top=120, bottom=120, left=200, right=160)
        
        fbp = fb_cell.paragraphs[0]
        fbp.paragraph_format.space_after = Pt(0)
        fbp.paragraph_format.line_spacing = 1.25
        for item_idx, item_text in enumerate(g_items):
            r_item = fbp.add_run(f"• 「{item_text}」\n" if "【備註】" not in item_text else f"• 「{item_text}\n")
            format_run(r_item, size_pt=9.5, italic=True if "【備註】" not in item_text else False, color_rgb=C_TEXT_DARK)

    p_spacer4 = doc.add_paragraph()
    p_spacer4.paragraph_format.space_after = Pt(10)

    # ------------------ 第三部分：講座檢討與未來場次籌備要點 ------------------
    h1_p3 = doc.add_paragraph()
    h1_p3.paragraph_format.space_before = Pt(16)
    h1_p3.paragraph_format.space_after = Pt(6)
    r_h1_p3 = h1_p3.add_run("第三部分：講座檢討與未來場次籌備要點 (Actionable SOP & Preparation)")
    format_run(r_h1_p3, size_pt=15.0, bold=True, color_rgb=C_PRIMARY_NAVY)

    p_sop_intro = doc.add_paragraph()
    p_sop_intro.paragraph_format.space_after = Pt(8)
    r_sop_intro = p_sop_intro.add_run("為確保未來承接各企業、公部門或巡檢機構之乳癌衛教時，能具備高標準、可複製、即調即用的作業水準，整合本次三場實務經驗，確立以下四大維度之標準作業方針（SOP）：")
    format_run(r_sop_intro, size_pt=10.0, color_rgb=C_TEXT_MUTED)

    # 維度一
    h2_d1 = doc.add_paragraph()
    h2_d1.paragraph_format.space_before = Pt(8)
    h2_d1.paragraph_format.space_after = Pt(4)
    r_d1 = h2_d1.add_run("維度一：簡報視覺標準與硬體相容驗收規範 (AV & Hardware SOP)")
    format_run(r_d1, size_pt=12.0, bold=True, color_rgb=C_SECONDARY_BLUE)
    
    d1_points = [
        ("投影片版面「大字滿版」鐵律", "全幅寬度嚴格鎖定於 16:9 比例，避免 3 欄或 4 欄之細碎文字塊。重點卡片（如 S7 外食餐盤、S10 公費判定、S15 切片工具、S16 七大警訊）一律採用「全寬雙欄」或「全螢幕單一焦點」，最小內文字級不得低於 18px，關鍵數據達 32~48px。動態位移樣式全面以純垂直 -translate-y-1 取代水平 scale 縮放，杜絕裁切風險。"),
        ("講者雙螢幕操作環境規範", "進場前確認快捷鍵分工：P 鍵開啟獨立滿版講者控制台（?view=speaker），講稿區設為特大行距，大螢幕畫面僅作為側邊輔助提示；F 鍵進入真·全螢幕；B 鍵於問答互動時一鍵黑屏控場。"),
        ("離線單頁穩定性確保", "簡報本體維持 100% 離線純 HTML/CSS/JS 單一檔案結構，零外網 CDN 依賴，即使廠區無 WiFi 阻擋亦能雙擊秒開正常播放。")
    ]
    for p_title, p_content in d1_points:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.25
        r_t = p.add_run(f"1. {p_title}：" if "大字" in p_title else (f"2. {p_title}：" if "雙螢幕" in p_title else f"3. {p_title}："))
        format_run(r_t, size_pt=10.0, bold=True, color_rgb=C_PRIMARY_NAVY)
        r_c = p.add_run(p_content)
        format_run(r_c, size_pt=9.5, color_rgb=C_TEXT_DARK)

    # 維度二
    h2_d2 = doc.add_paragraph()
    h2_d2.paragraph_format.space_before = Pt(10)
    h2_d2.paragraph_format.space_after = Pt(4)
    r_d2 = h2_d2.add_run("維度二：核心教學模組深化與進階案例擴充 (Curriculum Expansion)")
    format_run(r_d2, size_pt=12.0, bold=True, color_rgb=C_SECONDARY_BLUE)
    
    d2_points = [
        ("常設三大明星模組為黃金主幹", "根據問卷數據，壞習慣動態計算機（57.6%）、七大異常警訊（45.5%）與 BI-RADS 解碼（39.4%）為吸引力核心，未來各場次時間受限時應列為第一優先保留單元。"),
        ("新增「名人案例顯微鏡：安潔莉娜·裘莉與 BRCA 基因」模組", "回應聽眾對安潔莉娜·裘莉案例之高度興趣，於 S12（家族史）或 S13（高風險族群）增設此模組。涵蓋三大內容：\n• 事實解碼：家族多位親屬罹癌（母、阿姨、外婆），基因檢測證實 BRCA1 基因突變，評估終生乳癌風險達 87%（一般女性約 10~12%）。\n• 臨床決策圖：解構何謂「預防性雙側乳房切除重建術」vs「密集影像追蹤（每年乳房 MRI + 乳房攝影/超音波交替）」。\n• 關鍵帶走心態：「基因帶原不是得癌宣判，而是提前奪回健康主控權的情報。」")
    ]
    for p_title, p_content in d2_points:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.25
        r_t = p.add_run(f"1. {p_title}：" if "明星模組" in p_title else f"2. {p_title}：\n")
        format_run(r_t, size_pt=10.0, bold=True, color_rgb=C_PRIMARY_NAVY)
        r_c = p.add_run(p_content)
        format_run(r_c, size_pt=9.5, color_rgb=C_TEXT_DARK)

    # 維度三
    h2_d3 = doc.add_paragraph()
    h2_d3.paragraph_format.space_before = Pt(10)
    h2_d3.paragraph_format.space_after = Pt(4)
    r_d3 = h2_d3.add_run("維度三：課後行動轉化與醫療巡檢銜接機制 (Conversion & Follow-up SOP)")
    format_run(r_d3, size_pt=12.0, bold=True, color_rgb=C_SECONDARY_BLUE)
    
    d3_points = [
        ("主辦單位（廠區健管室／HR）72 小時聯防機制", "T+0 天（演講當日）於公司內網推播簡報線上隨身讀連結與問卷；T+3 天（黃金期）由健管室配合發送衛教追蹤信件，隨附：① 符合 114 年公費資格者（40 歲以上）廠區年度巡迴乳房攝影車登記表；② 未滿 40 歲或有家族史者敏盛醫院／國軍桃園總醫院乳房外科門診掛號指引。"),
        ("簡報 S25「榮譽通關證書」功能升級", "於證書介面新增「一鍵加入日曆提醒 (Google / Outlook / Apple Calendar)」，讓有意向之學員現場直接寫入 3 個月後之行事曆待辦事項。")
    ]
    for p_title, p_content in d3_points:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.25
        r_t = p.add_run(f"1. {p_title}：" if "72" in p_title else f"2. {p_title}：")
        format_run(r_t, size_pt=10.0, bold=True, color_rgb=C_PRIMARY_NAVY)
        r_c = p.add_run(p_content)
        format_run(r_c, size_pt=9.5, color_rgb=C_TEXT_DARK)

    # 維度四
    h2_d4 = doc.add_paragraph()
    h2_d4.paragraph_format.space_before = Pt(10)
    h2_d4.paragraph_format.space_after = Pt(4)
    r_d4 = h2_d4.add_run("維度四：演講現場行政與動線查核表 (Field Checklist)")
    format_run(r_d4, size_pt=12.0, bold=True, color_rgb=C_SECONDARY_BLUE)
    
    p_ck_desc = doc.add_paragraph()
    p_ck_desc.paragraph_format.space_after = Pt(4)
    r_ckd = p_ck_desc.add_run("開講前 30 分鐘，應逐一完成以下檢查項目：")
    format_run(r_ckd, size_pt=10.0, color_rgb=C_TEXT_MUTED)

    checklist_items = [
        ("硬體連線", "投影解析度確認（1920×1080 原生 16:9），確認投影幕最底行文字未被講台或前排觀眾遮擋。"),
        ("控台測試", "主螢幕與控制台筆電透過 BroadcastChannel 連線同步測試，驗證換頁延遲低於 0.1 秒。"),
        ("聲音調校", "無線麥克風音量與回音測試，保持溫和且具穿透力之講授音頻。"),
        ("網路與條碼", "手機現場掃描簡報首頁與尾頁 QR Code，確認離線講義網址與問卷 Google 表單均已開放。"),
        ("院所名片與衛教單張", "於講台或簽到桌備妥乳房外科門診時間表及公費攝影篩檢諮詢窗口。")
    ]
    for c_title, c_desc in checklist_items:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.2
        r_box = p.add_run("  ☑  ")
        format_run(r_box, size_pt=10.0, bold=True, color_rgb=C_ACCENT_TEAL)
        r_title = p.add_run(f"【{c_title}】")
        format_run(r_title, size_pt=9.5, bold=True, color_rgb=C_PRIMARY_NAVY)
        r_text = p.add_run(c_desc)
        format_run(r_text, size_pt=9.5, color_rgb=C_TEXT_DARK)

    p_spacer5 = doc.add_paragraph()
    p_spacer5.paragraph_format.space_after = Pt(12)

    # ------------------ 結論 ------------------
    h1_c = doc.add_paragraph()
    h1_c.paragraph_format.space_before = Pt(14)
    h1_c.paragraph_format.space_after = Pt(6)
    r_h1_c = h1_c.add_run("結論 (Conclusion)")
    format_run(r_h1_c, size_pt=15.0, bold=True, color_rgb=C_PRIMARY_NAVY)
    
    p_c = doc.add_paragraph()
    p_c.paragraph_format.space_after = Pt(6)
    p_c.paragraph_format.line_spacing = 1.3
    r_c = p_c.add_run(
        "本系列三場瑞健醫療巡迴講座，建立了結合「醫療專業實證」、「科技業邏輯對齊」與「高互動數位媒介」的衛教範例。本報告完整歸納數據真相與學員反饋，所提煉之視覺、內容、轉化及行政 SOP，將作為後續承接各類型企業健康講座與巡檢衛教的標準作業手冊，持續發揮早期篩檢、拯救生命的臨床實質效益。"
    )
    format_run(r_c, size_pt=10.5, color_rgb=C_TEXT_DARK)

    # 存檔
    output_path = "/Users/liangzuwei/Library/CloudStorage/GoogleDrive-spawnkiller1003@gmail.com/我的雲端硬碟/14_Antigravity2專案用/乳癌篩檢講座專案/乳癌篩檢衛教講座成效檢討與未來場次籌備報告.docx"
    doc.save(output_path)
    print(f"Document saved successfully at: {output_path}")

if __name__ == "__main__":
    create_report()

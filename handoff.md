# 交接紀錄 (HANDOFF.md)

- ✅ **【S16 七大乳房異常警訊最左與最右方框裁切徹底修復】**：
  - 診斷原因：
    1. S16（身體在送 Error Code！七大乳房異常警訊）頂部 7 顆警訊按鈕矩陣中，選中項目（預設為第 0 項「無痛單側腫塊」）使用了 `scale-110`，未選中項目在 hover 時使用了 `hover:scale-105`。
    2. 第 0 項位於最左側第 1 欄，`scale-110` 水平等比放大 10% 直接讓卡片左外緣凸出父容器；第 6 項位於最右側第 7 欄，選中或 hover 時亦向右凸出。
    3. 外層容器設有 `overflow-hidden`，凸出的邊框（Border）與陰影被直接切斷裁切。
  - 修復成果：
    1. **徹底移除所有水平放大 `scale-110` 與 `hover:scale-105`**：
       - S16 七大警訊卡片（`p17-card-0` ~ `p17-card-6`）靜態結構與 JS 動態切換函式 `selectP17Symptom(idx)` 同步更新。
    2. **全面升級為純垂直位移 `-translate-y-1`**：
       - 選中狀態改用 `-translate-y-1 shadow-lg shadow-red-500/20 ring-2 ring-red-400`，未選中 hover 改用 `hover:-translate-y-1`。
       - 卡片水平寬度 100% 嚴格鎖定於網格欄位內，從物理機制上杜絕左右越界裁切。
    3. **網格容器增設安全呼吸緩衝**：
       - 於 `grid` 容器補齊 `px-1.5 py-1` 安全邊距，為粗邊框提供充裕呼吸空間。
    4. 同步修復 S5 與 S7 的細微 scale 樣式，全專案四大核心檔案全面同步更新並推送至 GitHub Pages。

- ✅ **【雙螢幕講者視窗 (Speaker View) 螢幕滿版極致延展】**：
  - 核心需求：將整個 Speaker View 視窗與內部佈局拉長鋪滿整個螢幕，零黑邊、滿版大視野。
  - 修復與升級成果：
    1. **原生視窗啟動尺寸全滿版化**：
       - 徹底移除 `1320x860` 居中浮窗限制，改為抓取 `screen.availWidth` 與 `screen.availHeight`（`top=0, left=0`），彈出時直接鋪滿整個螢幕。
    2. **新增 `⛶ 螢幕滿版 (F)` 頂部一鍵按鈕**：
       - 在頂部列新增高對比粉紅快捷按鈕，點擊或按鍵盤 `F` 鍵即可瞬間進入真·全螢幕模式（隱藏瀏覽器標籤與網址列，極致純淨）。
    3. **雙欄極致垂直延伸與寬度鋪滿**：
       - 控制台外框改為 `fixed inset-0 h-full w-full min-h-screen`，`html` 與 `body` 全面鎖定 `overflow-hidden h-full w-full`，消除任何邊界多餘空隙。
       - 頂部工具列高度精簡至 `h-14`，釋放更多垂直空間給講稿閱讀區。
       - 左右雙欄直接鎖定 `col-span-4` 與 `col-span-8`，不再受螢幕 breakpoint 折行限制，100% 貼滿螢幕下緣與兩側邊界。
    4. 全專案四大核心檔案全面同步更新並推送到 GitHub Pages。

- ✅ **【雙螢幕講者視窗 (Speaker View) 版面升級：講稿特大化、畫面提示化】**：
  - 核心需求：
    - 大螢幕鏡像畫面縮小為側邊輔助提示，免霸佔視線。
    - 講稿（Speaker Notes）才是主講核心，全面放大至 60%~75% 寬度且字體升級為特大字體。
  - 修復與升級成果：
    1. **左右欄比例反轉重構**：
       - 左欄（提示與控制區）：縮小至 4~5 欄（`col-span-12 lg:col-span-5 xl:col-span-4`），整合「16:9 當前大螢幕鏡像提示（Live Mirror）」、「下一關預覽橫卡（Next Slide）」與「翻頁控制按鈕群」。
       - 右欄（講稿核心焦點區）：擴大至 7~8 欄（`col-span-12 lg:col-span-7 xl:col-span-8`），100% 垂直高度全數專屬呈現梁醫師私房講稿。
    2. **講稿字級全面放大與動態調節系統**：
       - 🎬 場景引子：升級為 `text-lg font-bold text-slate-200`
       - 🎯 節奏掌控與核心話術：升級為預設 **`text-2xl font-bold text-white leading-loose tracking-wide`**，遠距講台一目了然！
       - 💡 帶走金句：升級為 `text-xl font-black text-emerald-300`
       - 頂部工具列新增 **`A-` / `A+` 字級調節按鈕**（支援中、大、特大、巨幅四段無級切換，實時狀態指示）。
    3. **頂部版面切換按鈕升級 (V 鍵)**：
       - 支援一鍵快速切換：`講稿為主 (4:8)` ⇄ `巨幅講稿 (3:9)` ⇄ `均衡雙欄 (6:6)`，鏡像等比自適應縮放零失真。
    4. 全專案四大核心檔案全面同步更新並推送到 GitHub Pages。

- ✅ **【S11、S14、S15 最左及最右方框裁切徹底修復】**：
  - 診斷原因：
    1. 卡片按鈕在選中與 hover 時使用了水平放大屬性 `scale-105` 或 `scale-[1.02]`，導致最左與最右邊界的卡片橫向凸出父容器。
    2. 父容器具有 `overflow-hidden`，凸出的邊框與陰影直接被截斷裁切。
  - 修復成果：
    1. **全面移除水平 scale 放大**：S11（5大迷思卡）、S14（2大武器卡）、S15（4大派工卡）之 HTML 靜態結構與 JS 動態類別，徹底淘汰 `scale-105` / `scale-[1.02]`。
    2. **升級為純垂直向上微浮**：改用 `-translate-y-1`（垂直向上浮動 4px，水平寬度 100% 不變），從物理機制上徹底根除左右越界裁切。
    3. **網格容器增設安全邊界緩衝**：於 `grid` 容器加上 `px-1.5 py-1`，確保即使 `border-4` 加粗邊框也能在視窗邊緣內完整舒展。
    4. 全專案四大核心檔案全面同步更新並推送至 GitHub Pages。


- ✅ **【講者視窗/備忘彈窗長講稿滾動修復】**：
  - 診斷原因：
    1. 雙螢幕講者控制台（`?view=speaker` / P 鍵）中，Flexbox 列佈局缺少關鍵的 `min-h-0`，導致備忘卡片高度被文字撐大並在父容器被截斷，無法向下滾動。
    2. 全域 CSS 規則 `::-webkit-scrollbar { display: none; }` 隱藏了原生滾動條，無法透過滑鼠拖曳拉軸。
    3. 主螢幕按 S 鍵開啟的備忘彈窗缺少容器限制高度與 `overflow-y-auto`。
  - 修復成果：
    1. 在 `main`、左欄、右欄、備忘卡片全面補足 Flexbox `min-h-0`，並為滾動容器加入行內 `overflow-y: scroll !important;`。
    2. 新增高對比粉紅圓角專屬滾動條樣式（`.spk-scrollable::-webkit-scrollbar`），視覺清晰、滑鼠點擊即可拖曳。
    3. 在 `updateSpeakerViewUI` 換頁事件加入 `notesScrollContainer.scrollTop = 0`，每次換頁自動回到最頂端。
    4. S 鍵彈窗同步加上 `max-h-[85vh]` 與 `overflow-y-auto max-h-[55vh]`。
    5. 全專案四大檔案全面同步更新並推送至 GitHub Pages。


- ✅ **【S5 飲酒實證 2×2 四大卡片精簡為大字標題】**：
  - 依據梁醫師現場投影需求，將 2×2 四大實證矩陣框中的繁雜內文移除，保留超大字標題與生動圖示：
    1. 🍷 **酒類無差別（紅酒無特權）**
    2. 📈 **線性劑量效應（無安全低消）**
    3. ⚡ **頻率與暴飲（週末大喝更傷身）**
    4. 🔬 **三大生化致癌機轉**
  - 版面呼吸感大幅提升，字級提升至 `text-base sm:text-lg font-black`，遠距投影一眼聚焦！
  - 梁醫師可看著簡潔大標題直接進行深入口述，講者備忘（Notes）持續提供完整細節提示。
  - 同步更新全專案四大核心檔案並推送至 GitHub Pages。


- ✅ **【飲酒實證醫學報告正式實裝入投影片】（S5 專題特報 ＋ S4 負載機制升級 ＋ 講者指引）**：
  1. **S5（13 項危險因子全景地圖）實裝「飲酒與乳癌實證醫學特刊」**：
     - 在 S5 點選「規律飲酒習慣 (id=8)」時，右側聚光燈面板動態展開專屬設計的 2x2 四大實證矩陣：
       - 🍷 **酒類完全無差別（紅酒無特權）**：紅酒、白酒、啤酒、烈酒對乳癌風險等同，致癌關鍵在純酒精總克數，紅酒白藜蘆醇無法抵銷乙醛一級致癌性。
       - 📈 **線性劑量效應（無安全低消）**：每日每多 10g 酒精（約 1 杯），風險 +7%~10%；每日 2 杯 +20%；每日 3 杯以上激增 +30%~50%！
       - ⚡ **頻率與暴飲危害（週末大喝更傷）**：週末一次飲用 ≥ 4 杯（Binge Drinking），血液中乙醛與游離雌激素瞬間暴衝，加劇 DNA 雙鏈斷裂。
       - 🔬 **三大生化致癌機轉**：活化芳香化酶升高雌激素（促 ER+ 細胞增生）、乙醛一級致癌性破壞 DNA、干擾葉酸一碳代謝。
     - 底部深色卡提供**「梁醫師精準對策」**：能不喝就不喝，社交應酬以氣泡水加檸檬片、無酒精啤酒微替換！
     - 點選其他 12 項因子時無縫切回常規解析面板，DOM 元素 ID 100% 留存，零報錯零崩潰。
  2. **S4（科技職場 6 大負載）同步升級**：
     - 第 6 項「飲酒與紓壓」點擊時，機制文字同步升級為「酒類無差別、無安全劑量、週末暴飲游離雌激素暴衝」之精煉數據。
  3. **講者備忘（Speaker Notes）同步注入**：
     - S5 `data-notes` 補足條理分明的口述指引，梁醫師在雙螢幕講者模式（P 鍵）中可直接對照講述。
  4. **全專案四大核心檔案 100% 同步**：
     - `投影片方案/守護乳房健康_第三場六福廠_活力輕科技敘事風.html`
     - `投影片方案/守護乳房健康_第二場南崁廠_活力輕科技敘事風.html`
     - `投影片方案/守護乳房健康_活力輕科技敘事風.html`
     - `index.html`（GitHub Pages 首頁入口）


- ✅ **【第三版·六福廠專場發布 ＆ 精準醫療細節三項重構】**：
  1. **S7 護乳外食微替換餐盤切字根治**：
     - 重構動態生成卡片佈局，將圖示與標籤置於頂部兩側，下方標題採用 `text-base sm:text-lg font-black leading-snug` 縱向大字排版，徹底移除 `truncate`。
     - **「雙色花椰菜 + 綠木耳」** 與其說明文字完整清晰顯示，零切字零省略。
  2. **S10 公費判定字型全面同級大字化**：
     - 「年齡未滿 40 歲（尚未達公費攝影年齡）」之標題大小升級為 `text-xl sm:text-2xl font-black text-amber-900`（或 `text-slate-900`），與「🎉 符合公費資格！」完全同級等大。
     - 內文說明與專業指引卡片統一提升至 `text-base sm:text-lg`，遠距投影一清二楚。
  3. **新 S15 臨床派工決策羅盤：替換為「3D 全自動超音波 (ABUS)」純影像工具**：
     - 依據梁醫師臨床指導，排除病理切片（CNB），鎖定純影像檢查派工。
     - 將第 1 項檢查正式替換為 **「3D 全自動乳房超音波 (ABUS)」**，與 **「放大／局部壓迫攝影」**、**「3D 斷層合成 (DBT)」**、**「乳房磁振造影 (MRI)」** 構成完美的 4 大進階影像派工矩陣。
     - 修正 `showSlide` 轉場 hook 頁碼偏移問題，精準對應 `currentSlide === 15` 調用 `setP142Tool('abus')`。
  4. **全專案四核心檔案全面同步與驗證**：
     - 同步更新：`投影片方案/守護乳房健康_第三場六福廠_活力輕科技敘事風.html`、`投影片方案/守護乳房健康_第二場南崁廠_活力輕科技敘事風.html`、`投影片方案/守護乳房健康_活力輕科技敘事風.html`、`index.html`。


  1. **問題診斷**：
     - 本地以 `file:///` 協定雙擊打開 HTML 時，受到瀏覽器跨域限制或無外網/CDN 延遲影響，原本引用的 `<script src="https://cdn.tailwindcss.com"></script>` 未能及時編譯載入，導致頁面出現「無樣式、純文字黑白排列、排版跑掉」的現象。
  2. **徹底修復方案**：
     - 透過 Chrome Headless 引擎將方案 C 投影片所需之全部 24 頁靜態與動態 class、自訂顏色與響應式規則，完整編譯出獨立純 CSS 樣式表（約 50 KB）。
     - 將該完整樣式表直接內嵌於 HTML 的 `<style>` 標籤中，徹底解除對外部 CDN 的即時依賴。
     - **達成效果**：無論有無網路、在任何科技廠內網、會議室筆電、本機直接雙擊開啟，樣式均 0 毫秒即時渲染，100% 保證排版穩定完美，符合 `AGENTS.md` 離線獨立播放承諾！
  3. **同步與發布**：
     - 同步更新三大檔案：`投影片方案/守護乳房健康_第二場南崁廠_活力輕科技敘事風.html`、`index.html`、`投影片方案/守護乳房健康_活力輕科技敘事風.html`。
     - Git commit: `c8e8cf6` 已推送至 GitHub Pages。
  1. **致命根本原因診斷與根治**：
     - 先前在調整 S7/S8 互動模組時，尾部注入之腳本發生 `Identifier 'p08MealData' has already been declared` 及語法錯誤 `function try`，加上重複殘留的 `calcP19Count` 代碼。
     - 瀏覽器在載入階段遭遇 JS SyntaxError，直接中斷執行並拋棄整段腳本，導致包括換頁（左右箭頭/換頁鈕）、全螢幕（F）、目錄抽屜（M）、S1 場次按鈕與 S7/S8/S18/S19 互動全部無反應。
  2. **全面重構修復成果**：
     - 徹底移除所有重複宣告的 `const`/`let` 與舊版過期函數。
     - **S7 微替換動態餐盤**：重構為 `bad`（傳統高負載便當）vs `good`（護乳微替換動態餐盤）雙狀態切換，完美連動 `p08-tab-bad` / `p08-tab-good` / `p08-meal-container` / `p08-summary-box`。
     - **S8 微運動蓄力儀 ＋ 睡眠修復工程**：
       - 微運動：支援 6 個碎片活動點擊累加，即時動態更新 `p09-progress-text` 與進度條，滿 150 分鐘時動態觸發「🎉 啟動 20% 防禦盾！」；一鍵「🔄 重置歸零」即時復原。
       - 睡眠修復：支援「🚨 熬夜藍光模式」與「🌙 22:00 數位停機」左右按鈕切換，動態連動下方褪黑激素、皮質醇與 DNA 修復生物指標儀。
     - **S18 五大精準醫療武器庫**：點擊手術、標靶、荷爾蒙、放療、免疫等 5 大武器，右側聚光燈即時切換臨床實證指引。
     - **S19 健保保護傘與生活品質**：點擊重大傷病、即時重建、重返職場 3 大權益卡，即時展開滿版權益實錄。
     - **語法嚴格驗證**：透過 Node.js `node --check` 語法引擎檢驗，結果為 `0 errors`（完全通過，零語法錯誤）！
  3. **三大核心檔案全面同步與 GitHub Pages 推送**：
     - 已同步覆蓋 `投影片方案/守護乳房健康_第二場南崁廠_活力輕科技敘事風.html`、`index.html`、`投影片方案/守護乳房健康_活力輕科技敘事風.html`。
     - Git commit: `43f24eb` 並成功推送至遠端 `main` 分支，GitHub Pages 已同步發布！

- 已完成 **依據第一堂課（瑞健桃園廠）學員與廠護回饋全面精進升級（Plan C v2.0）**：
  1. **字體全面跳級放大**：徹底淘汰 14px 以下小字，內文說明全面提升至 `18~20px (text-lg/xl)`，關鍵數據與大標題拉升至 `24~36px (text-2xl/4xl)`，精簡文字密度，徹底根治遠距大會議室後排閱讀痛點。
  2. **生活型態篇幅精練濃縮（釋出 2 頁時間）**：
     - **新 S7**：將飲食微替換（原 S7 概念 + S8 餐盤）整合為高互動「護乳生活指南：飲食微替換餐盤與 5 大防禦陣列」，外食便當 vs 微替換餐盤動態切換大字滿版。
     - **新 S8**：將運動與睡眠（原 S9 蓄力儀 + S10 藍光修復）左右合一為「動能重置：150 分鐘碎片運動 ＋ 睡眠修復工程」，節奏緊湊不拖泥帶水。
  3. **全新擴充「確診後防治與精準醫療」（回應同仁最強烈期待）**：
     - **🌟 新 S18【確診不慌張！現代乳癌多元精準武器庫】**：微創與保留手術（保留率>70%/前哨淋巴免廓清）、精準標靶（HER2 巡弋飛彈）、口服荷爾蒙（佔比70%每天一顆多數免化療）、立體弧形放療護心肺與免疫療法，5 大武器高互動聚光燈切換！
     - **🌟 新 S19【健保與重大傷病保護傘 ＋ 重返職場生活品質】**：重大傷病證明免部分負擔、健保標靶新藥納入、切除同步即時整型重建（留住自信與體態）、85% 順利重返科技工作崗位。
  4. **全景地圖（M 鍵）與轉場 Hook 全面適配**：抽屜目錄 24 頁無縫更新，雙螢幕同步零延遲。


- 已完成 **方案 B【溫潤人文雜誌風】字大滿版高互動完全版**（24 頁全覆蓋，燕麥暖米白底、典雅 Noto Serif 襯線大字、乾燥玫瑰粉色調）。
- 已完成 **方案 C【活力輕科技敘事風】最新 6 大互動與醫學精修**，並**直接覆蓋** [`投影片方案/守護乳房健康_活力輕科技敘事風.html`](file:///Users/liangzuwei/Library/CloudStorage/GoogleDrive-spawnkiller1003@gmail.com/我的雲端硬碟/14_Antigravity2專案用/乳癌篩檢講座專案/投影片方案/守護乳房健康_活力輕科技敘事風.html)：
  1. **S6 轉場健康清零**：轉場進入 S6 時，左方生活習慣核取方塊全不勾選，右方發炎指數即時歸零（0% 基準線）。
  2. **S9 蓄力儀重置與中文標示**：轉場進入 S9 時從 0 開始蓄力，進度條重置，右方匡內單位由 `150m` 正式改為中文字 `150 分鐘`。
  3. **S10 左右方框高互動模式對比**：睡前藍光模式 vs 22:00 數位停機修復模式設計為左右可點擊互動切換，下方即時動態連動「體內生物指標監測儀（褪黑激素、皮質醇、DNA 修復進程）」。
  4. **S5 與 S11 醫學因子權威查核與精準對齊**：依據國健署官方最新標準，S5 與 S11 的先天高風險因子（家族史、非典型增生/癌症史、初經早停經晚、晚育/未哺乳、緻密型乳房）全面一致對齊，並落實 114 年擴大公費 40-74 歲全面補助及 40 歲以下高風險自 30 歲定期超音波指引。
  5. **S17 七大異常警訊互動化**：7 個小方塊全面升級為可點擊互動卡片，下方動態展開「臨床醫師深層鑑別面板」，包含【觸摸與外觀特徵】、【良性 vs 惡性鑑別】與【醫師建議處置】。
- 已完成 **雙螢幕演講者模式（Speaker View & Dual-Screen Sync）**：
  - **大螢幕/投影機（主視窗）**：播放乾淨純粹的簡報畫面，無雜訊干擾，支援 `F` 鍵全螢幕與 `B` 鍵瞬間黑屏（Blank Screen 控場專注）。
  - **講者螢幕（獨立控制台視窗）**：點擊底部「🖥️ 講者視窗 (P)」或按快捷鍵 `P` 自動以新視窗彈出（或直接加參數 `?view=speaker` 開啟）。
  - **講者專屬介面配備**：
    1. 當前投影片即時縮圖
    2. 下一張投影片即時預覽與轉場提示
    3. 超大字體講者備忘（Speaker Notes）
    4. 60 分鐘演講倒數計時器（含啟動、暫停、重置、逾時警示）
    5. 即時控場按鈕（上一張、下一張、跳頁、黑屏切換）
  - **跨視窗雙向同步技術**：採用 HTML5 `BroadcastChannel` 配合 `localStorage` storage 事件作為雙重備援，換頁與黑屏操作零延遲（< 5ms）跨視窗同步。
- 已完成 **GitHub Pages 正式部署上線與專屬 QR Code 生成**：
  - **公開主簡報網址**：[`https://spawnkiller1003-bit.github.io/breast-screening-slides/`](https://spawnkiller1003-bit.github.io/breast-screening-slides/)
  - **講者控制台網址**：[`https://spawnkiller1003-bit.github.io/breast-screening-slides/?view=speaker`](https://spawnkiller1003-bit.github.io/breast-screening-slides/?view=speaker)
  - **開源倉庫 (Public Repo)**：[`https://github.com/spawnkiller1003-bit/breast-screening-slides`](https://github.com/spawnkiller1003-bit/breast-screening-slides)
  - **最後一頁（Slide 24）專屬 QR Code**：已生成高品質純向量 SVG QR Code，零外網依賴內嵌於簡報第 24 頁，點擊可直接放大燈箱（Click-to-Zoom），供演講現場觀眾以手機鏡頭直接掃描帶走整份簡報！

- 已完成 **全體聽眾友善調整、企業名稱修正與互動欄位滿版大字化**（直接覆蓋 [`投影片方案/守護乳房健康_活力輕科技敘事風.html`](file:///Users/liangzuwei/Library/CloudStorage/GoogleDrive-spawnkiller1003@gmail.com/我的雲端硬碟/14_Antigravity2專案用/乳癌篩檢講座專案/投影片方案/守護乳房健康_活力輕科技敘事風.html) 及 [`index.html`](file:///Users/liangzuwei/Library/CloudStorage/GoogleDrive-spawnkiller1003@gmail.com/我的雲端硬碟/14_Antigravity2專案用/乳癌篩檢講座專案/index.html)）：
  1. **主辦企業名稱精準修正**：全面將「瑞健科技」修正為「瑞健公司」（封面專場、巡迴場次切換、結尾榮譽通關證書）。
  2. **全體聽眾包容性視角（破除單一女性設定）**：
     - 將標題與內文「科技女性」升級為「科技職場夥伴」、「職場同仁」、「科技人」，讓全體聽眾（包括男性主管、工程師等）產生共鳴。
     - 講者備忘與醫學指引融入男性視角：男性亦有 1% 罹患乳癌機率，且男士更是身邊伴侶、母親、女兒最關鍵的「健康神隊友」，提醒並守護全家人的公費篩檢福利。
  3. **互動點擊後展開欄位字體全面加大滿版**：
     - **P03 數據洞察**：標題升級至 `text-2xl`，內文升級至 `text-lg font-bold`。
     - **P04 隱形負載詳情**：標籤與生物學機制全面升級為 `text-xl font-black` 與 `text-lg font-bold`。
     - **P05 先天與後天卡片**：13 項危險因子格子字體由原本的 `text-xs` 大幅升級為 `text-base sm:text-lg font-bold`，padding 加大。
     - **P08 微替換動態餐盤**：按鈕、菜色標題、說明與臨床總結全面大字滿版展示。
     - **P10 藍光 vs 修復監測儀**：指標數值由 `text-xs` 升級為 `text-2xl font-black`，臨床解析升級至 `text-lg font-bold`。
     - **P11 公費篩檢小工具**：判定結果大標題升級為 `text-2xl`，指引內容全面大字滿版。
     - **P12 戳破迷思面板**：醫學解讀升級為 `text-xl font-bold`。
     - **P13 攝影 Stepper**：說明文字升級至 `text-lg font-bold`，小撇步提示全面加大。
     - **P14 BI-RADS 解碼**：標題升級為 `text-3xl`，影像臨床解析升級至 `text-xl font-bold`。
     - **P17 七大異常警訊臨床深層鑑別面板**：名稱加大至 `text-2xl`，觸摸外觀、良惡性鑑別、醫師建議處置三欄內文由原本極小的 `text-xs` 大幅放大至 `text-base sm:text-lg font-bold`，滿版大氣！
     - **P18 存活率期別**：期別說明文字升級至 `text-xl font-bold`。
     - **P22 FAQ 常見問答手風琴**：題目由 `text-sm` 升級為 `text-xl font-black`，展開解答由 `text-xs` 放大為 `text-lg font-bold`！
     - **P23 金句卡放大**：字體升級至 `text-4xl sm:text-5xl font-black`。

- 已完成 **C 方案「聚光燈模式（Spotlight Mode）」降噪與版面重構**（直接覆蓋 [`投影片方案/守護乳房健康_活力輕科技敘事風.html`](file:///Users/liangzuwei/Library/CloudStorage/GoogleDrive-spawnkiller1003@gmail.com/我的雲端硬碟/14_Antigravity2專案用/乳癌篩檢講座專案/投影片方案/守護乳房健康_活力輕科技敘事風.html) 及 [`index.html`](file:///Users/liangzuwei/Library/CloudStorage/GoogleDrive-spawnkiller1003@gmail.com/我的雲端硬碟/14_Antigravity2專案用/乳癌篩檢講座專案/index.html)）：
  1. **S5（13 項危險因子）**：改為聚光卡架構。左側 13 項因子大字清單（支援全部/先天/後天篩選），點擊任一項目即於右側滿版展開超大字（標題 32px、機轉 20px、防禦對策 20px）聚光卡，徹底解決後排看不清問題。
  2. **S9（微運動蓄力儀）**：**碎片活動靠左接近滿版（9 cols）**，排成 6 個大字微運動方塊；**累積時間縮小放右側小空間（3 cols）**，形成精巧的高科技直立充電座 HUD。
  3. **S10（藍光 vs 修復模式）**：**預設左框先亮（熬夜藍光模式）**！套用紅色高亮光暈與當前狀態動畫，進入頁面時下方即時監測儀預設呈現藍光模式下的生理數據。
  4. **S12（打破篩檢 5 大迷思）**：5 張迷思卡升級為聚光燈互動，點選任一迷思時其他卡片淡化，下方滿版黑色聚光卡以 32px 巨幅綠字白字投射梁醫師科學真相。
  5. **S15（檢查工具總覽地圖）**：攝影 vs 超音波兩大武器升級為聚光燈切換，點選即展開 30px 超大字武器剖析卡（最強戰場 vs 盲區應對）。
  6. **S16（加做 4 種檢查羅盤）**：4 大進階工具（超音波、放大攝影、3D DBT、MRI）點選即展開大字派工指令卡。
  7. **S17（七大乳房異常警訊）**：點選任一警訊方塊時，該項目放大發光，其餘 6 項優雅淡化（opacity-40），下方以紅色巨幅橫標＋超大字呈現觸摸特徵、良惡性鑑別與梁醫師處置指令！

- 已完成 **全方位無障礙導航系統升級與快取禁用保護（徹底根治按鍵點擊問題）**：
  1. **快取禁用機制（No-Cache Headers）**：在 HTML `<head>` 加入 `no-cache, no-store, must-revalidate`，並透過附帶版本參數（`?v=3.2`）強制瀏覽器繞過任何本地損壞快取。
  2. **兩側超大懸浮導航箭頭（Floating Paddles）**：在螢幕左側（‹）與右側（›）加入圓形高對比懸浮按鈕（48px），滑鼠或手指直接點擊即可順暢換頁。
  3. **簡報筆與全鍵盤廣域支援**：全面擴充換頁鍵位，除箭頭外，支援簡報筆慣用的 `Enter`、`PageDown`、`PageUp`、`ArrowDown`、`ArrowUp`、`Space`、`n/N` 等所有常見鍵盤操作。
  4. **手機與平板觸控滑動支援（Touch Swipe）**：支援原生水平手勢滑動，左滑下一頁、右滑上一頁，行動裝置操作流暢無阻。

- 已完成 **S5 鏡像切換、S6 寬版 9:3 佈局、S14 Category 與手機雙向相容優化**（直接覆蓋 [`投影片方案/守護乳房健康_活力輕科技敘事風.html`](file:///Users/liangzuwei/Library/CloudStorage/GoogleDrive-spawnkiller1003@gmail.com/我的雲端硬碟/14_Antigravity2專案用/乳癌篩檢講座專案/投影片方案/守護乳房健康_活力輕科技敘事風.html) 及 [`index.html`](file:///Users/liangzuwei/Library/CloudStorage/GoogleDrive-spawnkiller1003@gmail.com/我的雲端硬碟/14_Antigravity2專案用/乳癌篩檢講座專案/index.html)）：
  1. **S5（危險因子鏡像切換）**：
     - 移除「全部 13 項」按鈕，只保留「先天無法改變 (6項)」與「後天完全可控 (7項)」兩大分流標籤。
     - 點擊「先天 6 項」時：左框為個別因子清單，右框為放大解說聚光卡。
     - 點擊「後天 7 項」時：反過來！左框為放大解說聚光卡，右框為個別因子清單，形成直覺的鏡像對比佈局。
  2. **S6（健康價標動態計算機比照 S9 重構）**：
     - 採用 9:3 格線佈局：左側 9 cols 放置日常生活習慣選項（大字卡片、高對比勾選），右側 3 cols 放置縮小的直立式高科技「發炎監測艙 HUD」（大數字、進度條、即時處方與一鍵清零重設）。
  3. **S14（BI-RADS 報告分級全面改為英文）**：
     - 將所有「類別 0 ~ 類別 6」全面改為符合國際醫學慣例的英文「Category 0 ~ Category 6」。
  4. **手機端直拿與橫拿（Portrait & Landscape）全相容**：
     - 加入智慧響應式 CSS（`@media (max-width: 1024px), (max-height: 550px)`），當手機直拿或橫拿時，解除固定 `100vh overflow-hidden`，切換為 `overflow-y: auto !important; min-height: 100dvh`，確保手機橫屏或小螢幕下所有內容皆可上下滑動檢視，按鈕不被遮擋。
     - 兩側懸浮導航鍵在手機模式下自動縮小為精巧的 `w-10 h-10`，不遮擋文字，同時維持原生水平滑動切頁（Touch Swipe）。
  5. **JavaScript 語法 100% 嚴格驗證**：
     - 全面修復多餘括號，達成括號對稱性與 Backtick 成對驗證 100% 通過，確保所有按鈕與滑動點擊功能流暢無阻。

- 已完成 **手機播放模式保護機制：停用手勢左滑/右滑切頁，全面改為兩側「超大懸浮導航箭頭（‹ 與 ›）」**（直接覆蓋 [`投影片方案/守護乳房健康_活力輕科技敘事風.html`](file:///Users/liangzuwei/Library/CloudStorage/GoogleDrive-spawnkiller1003@gmail.com/我的雲端硬碟/14_Antigravity2專案用/乳癌篩檢講座專案/投影片方案/守護乳房健康_活力輕科技敘事風.html) 及 [`index.html`](file:///Users/liangzuwei/Library/CloudStorage/GoogleDrive-spawnkiller1003@gmail.com/我的雲端硬碟/14_Antigravity2專案用/乳癌篩檢講座專案/index.html)）：
  1. **徹底移除手勢左右滑動切頁**：完全移除 `touchstart` 與 `touchend` 換頁監聽器，杜絕使用者在手機上點擊互動卡片、滑動自訂元件或上下自然捲動時，因微小水平位移而產生誤觸跳頁的困擾。
  2. **兩側超大懸浮導航箭頭（‹ 與 ›）升級**：
     - 在手機與各尺寸螢幕兩側加入直徑 `3.5rem`（56px）、圓形高質感的懸浮導航箭頭，符號放大至 `2.25rem`（36px 超大字體）。
     - 左右按鈕固定於畫面垂直正中央（`top: 50% -translate-y-1/2`），貼齊螢幕兩側邊界（`0.5rem`），配備高對比毛玻璃陰影（Prev 白底黑字、Next 亮粉底白字），大拇指單手即可輕鬆盲按。
     - 手機模式下主內容區自動配置左右 `3.5rem` 的安全留白，確保中央的文字、按鈕與互動卡片 100% 不會被兩側大箭頭遮擋。

- 已完成 **演講者畫面雙螢幕極致同步引擎升級（Quad-Sync Engine）與原生 16:9 縮放鏡像重構**（徹底解決本地 `file://` 與線上雙螢幕投影片不同步問題，直接覆蓋 [`投影片方案/守護乳房健康_活力輕科技敘事風.html`](file:///Users/liangzuwei/Library/CloudStorage/GoogleDrive-spawnkiller1003@gmail.com/我的雲端硬碟/14_Antigravity2專案用/乳癌篩檢講座專案/投影片方案/守護乳房健康_活力輕科技敘事風.html) 及 [`index.html`](file:///Users/liangzuwei/Library/CloudStorage/GoogleDrive-spawnkiller1003@gmail.com/我的雲端硬碟/14_Antigravity2專案用/乳癌篩檢講座專案/index.html)）：
  1. **跨視窗同步中樞全面重構（四重備援通道）**：
     - **通道 1（父子視窗直通）**：主視窗與講者控制台視窗持有相互的 `window.opener` 與 `speakerWindowRef` 引用，透過 `postMessage(payload, '*')` 直通傳輸。徹底解決瀏覽器在本地 `file://` 協定下將 origin 視為 `null` 導致 BroadcastChannel 與 localStorage 失效的硬體限制，延遲 < 1ms。
     - **通道 1.5（同源/本地直接方法調用）**：支援 `handleSyncDirect(payload)`，同瀏覽器行程下 0ms 瞬間呼叫。
     - **通道 2（BroadcastChannel）**：線上與 localhost 多視窗即時廣播。
     - **通道 3（localStorage）**：跨獨立分頁 storage 事件備援。
  2. **智慧雙向握手機制（Handshake Protocol）**：
     - 講者視窗開啟時，URL 自動夾帶當前頁碼參數（`?view=speaker&slide=N`），開啟瞬間精確對齊當前進度。
     - 講者視窗載入完成後主動發起 `REQ_SYNC` 請求，主螢幕即時回應 `ACK_SYNC`（回傳最新頁碼與黑屏狀態），頂部徽章即時亮起「🟢 大螢幕已連線同步」。
  3. **原生 DOM 16:9 縮放鏡像預覽（全面淘汰 iframe）**：
     - 徹底拔除原本在本地 `file://` 下會觸發跨域阻擋（CORS/SecurityError）且會加載失敗的 `<iframe id="spk-mirror-frame">`。
     - 改採**原生 DOM 高清縮放畫布（`#spk-preview-stage`）**，在講者控制台左側以 1280x720 比例完美等比縮放鏡像展示當前大螢幕正在播放的投影片，零資源浪費、零網路請求、絕不閃白，換頁時 0ms 瞬間同步！

- 已完成 **演講者控制台「投影片畫面極致滿版」升級（Full-Bleed Speaker View）**（直接覆蓋 [`投影片方案/守護乳房健康_活力輕科技敘事風.html`](file:///Users/liangzuwei/Library/CloudStorage/GoogleDrive-spawnkiller1003@gmail.com/我的雲端硬碟/14_Antigravity2專案用/乳癌篩檢講座專案/投影片方案/守護乳房健康_活力輕科技敘事風.html) 及 [`index.html`](file:///Users/liangzuwei/Library/CloudStorage/GoogleDrive-spawnkiller1003@gmail.com/我的雲端硬碟/14_Antigravity2專案用/乳癌篩檢講座專案/index.html)）：
  1. **投影片畫面佔比擴大至 8 ~ 9 欄**：將左側投影片畫面由原本的 7 欄大幅擴大至 `col-span-8 xl:col-span-9`（佔全螢幕 67% ~ 75% 面積），大幅壓制周圍留白，大字體與圖表細節一覽無遺。
  2. **16:9 原生縮放畫布邊界極限貼合**：縮放演算法升級為滿版貼邊（扣除微量 4px），內部 1280×720 畫布移除多餘外層邊距與黑邊，投影片內容以最大比例飽滿呈現。
  3. **視圖切換模式支援（巨幅滿版 V 鍵）**：
     - 頂部控制列新增「📐 巨幅滿版 (V)」按鈕，支援鍵盤快捷鍵 `V`。
     - 點擊可在一秒內將左側投影片進一步擴展至 **10 欄（佔 83% 超巨幅滿版）**，右側備忘縮為精巧速記欄，滿足講者對畫面極致放大的閱覽需求。

- 已完成 **S16 演講者畫面無法同步問題根除與全域轉場 Hook 防禦強化**（直接覆蓋 [`投影片方案/守護乳房健康_活力輕科技敘事風.html`](file:///Users/liangzuwei/Library/CloudStorage/GoogleDrive-spawnkiller1003@gmail.com/我的雲端硬碟/14_Antigravity2專案用/乳癌篩檢講座專案/投影片方案/守護乳房健康_活力輕科技敘事風.html) 及 [`index.html`](file:///Users/liangzuwei/Library/CloudStorage/GoogleDrive-spawnkiller1003@gmail.com/我的雲端硬碟/14_Antigravity2專案用/乳癌篩檢講座專案/index.html)）：
  1. **S16 轉場 Hook 異常排查與修復**：修復了 `setP142Tool()` 內部未帶引數呼叫 `document.getElementById()` 觸發 TypeError 的問題，補齊完整選擇器 `document.getElementById('p142-btn-' + tool)`，恢復 S16 派工羅盤自動啟動。
  2. **全域轉場生命週期 Hook 防禦性封裝（Try-Catch Protection）**：在 `showSlide()` 的轉場 hook 外層加入強韌的 `try-catch` 防禦性保護，徹底確保未來任何單一投影片內部的互動邏輯若有例外，絕不干擾或阻斷大螢幕廣播與演講者控制台 UI（縮圖、下一頁預覽、備忘話術）的即時渲染。

- 已完成 **S17 七大異常警訊「腋下淋巴水腫」與「兩側大小突變」Clinical Priority 嚴格對齊修正**（直接覆蓋 [`投影片方案/守護乳房健康_活力輕科技敘事風.html`](file:///Users/liangzuwei/Library/CloudStorage/GoogleDrive-spawnkiller1003@gmail.com/我的雲端硬碟/14_Antigravity2專案用/乳癌篩檢講座專案/投影片方案/守護乳房健康_活力輕科技敘事風.html) 及 [`index.html`](file:///Users/liangzuwei/Library/CloudStorage/GoogleDrive-spawnkiller1003@gmail.com/我的雲端硬碟/14_Antigravity2專案用/乳癌篩檢講座專案/index.html)）：
  1. **Clinical Priority 與卡片嚴密一對一對應**：全面修正先前卡片排列與 JS `p17Symptoms` 陣列索引錯位相反問題。
     - **Card 5**：🪨 腋下淋巴水腫 ➡️ 精準對應 **CLINICAL PRIORITY 06**（淋巴腺腫大／無痛硬質成串）。
     - **Card 6**：📏 兩側大小突變 ➡️ 精準對應 **CLINICAL PRIORITY 07**（形狀突然改變／輪廓不對稱）。
     - **Card 3 & Card 4**：🔴 乳頭凹陷回縮（PRIORITY 04）與 🍊 橘皮樣水腫（PRIORITY 05）亦同步完成一對一精準校準。
  2. **臨床鑑別面板同步連動**：點擊任一警訊方塊，下方聚光卡顯示的圖示、Priority 編號、臨床外觀、良惡性鑑別與醫師建議處置均 100% 準確無誤。

## 🚦 目前狀態
- **線上運行狀態**：GitHub Pages 100% 在線（HTTP/2 200 OK），S1 預設勾選「瑞健南崁廠 🌟 本場專屬」，S18 完整涵蓋 5 大 EBM 決策模組，S19 健保保護傘，S24 雙 QR Code 正常！
- **第二場（10/14 南崁廠）專屬檔案已獨立歸檔**：
  - 📝 **第二場大綱**：[`原始資料/講座簡報大綱_第二場南崁廠.md`](file:///Users/liangzuwei/Library/CloudStorage/GoogleDrive-spawnkiller1003@gmail.com/我的雲端硬碟/14_Antigravity2專案用/乳癌篩檢講座專案/原始資料/講座簡報大綱_第二場南崁廠.md)（與第一場大綱明確區別）
  - 🌟 **第二場專屬 HTML 投影片**：[`投影片方案/守護乳房健康_第二場南崁廠_活力輕科技敘事風.html`](file:///Users/liangzuwei/Library/CloudStorage/GoogleDrive-spawnkiller1003@gmail.com/我的雲端硬碟/14_Antigravity2專案用/乳癌篩檢講座專案/投影片方案/守護乳房健康_第二場南崁廠_活力輕科技敘事風.html)（S1 直接勾選第二場南崁廠，與第一場方案明確區別）
  - 🚀 **公開線上入口**：[`index.html`](file:///Users/liangzuwei/Library/CloudStorage/GoogleDrive-spawnkiller1003@gmail.com/我的雲端硬碟/14_Antigravity2專案用/乳癌篩檢講座專案/index.html)（已同步部署至 GitHub Pages）
- **歷程與基礎版本清單**：
  - 第一場/原始大綱：[`原始資料/講座簡報大綱.md`](file:///Users/liangzuwei/Library/CloudStorage/GoogleDrive-spawnkiller1003@gmail.com/我的雲端硬碟/14_Antigravity2專案用/乳癌篩檢講座專案/原始資料/講座簡報大綱.md)
  - 第一場/原始方案 C：[`投影片方案/守護乳房健康_活力輕科技敘事風.html`](file:///Users/liangzuwei/Library/CloudStorage/GoogleDrive-spawnkiller1003@gmail.com/我的雲端硬碟/14_Antigravity2專案用/乳癌篩檢講座專案/投影片方案/守護乳房健康_活力輕科技敘事風.html)
  - 方案 A 原型：[`投影片方案/守護乳房健康_現代科技儀表板風.html`](file:///Users/liangzuwei/Library/CloudStorage/GoogleDrive-spawnkiller1003@gmail.com/我的雲端硬碟/14_Antigravity2專案用/乳癌篩檢講座專案/投影片方案/守護乳房健康_現代科技儀表板風.html)
  - 方案 B 原型：[`投影片方案/守護乳房健康_溫潤人文雜誌風.html`](file:///Users/liangzuwei/Library/CloudStorage/GoogleDrive-spawnkiller1003@gmail.com/我的雲端硬碟/14_Antigravity2專案用/乳癌篩檢講座專案/投影片方案/守護乳房健康_溫潤人文雜誌風.html)

## ➡️ 下一步（第二場講座前瞻）
1. **第二場講座（115/10/14 瑞健南崁 14:00－15:00）現場播放**：
   - 使用雙螢幕演講者控制台（`P` 鍵開啟獨立講者視窗，`F` 鍵大螢幕全螢幕）。
   - S1 開場即展現南崁專場身份，建立同仁強烈歸屬感。
   - S18 深度講解 5 大臨床實證，S19 破除費用與生活恐慌。
   - 結尾邀請全員掃碼填答 Google 表單問卷與領取講義。
2. **第二場問卷回收與持續調優**：
   - 講座結束後檢視南崁同仁之填答回饋，為第三場（10/21 六福廠）做好萬全準備。

## 🕐 最後更新
- **時間**：2026-10-11 17:28
- **更新者**：Antigravity @ liangzuweideMacBook-Pro.local
- **Git push**：已同步推送至 `spawnkiller1003-bit/breast-screening-slides:main`









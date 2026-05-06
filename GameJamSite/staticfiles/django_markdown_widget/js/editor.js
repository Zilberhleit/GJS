(function () {
  "use strict";

  // ---------------------------------------------------------------------------
  // 1. TOOLBAR_BUTTONS
  // ---------------------------------------------------------------------------
  const TOOLBAR_BUTTONS = {
    heading: { icon: '<svg viewBox="0 0 16 16" width="16" height="16"><path fill="currentColor" d="M3.75 2a.75.75 0 0 1 .75.75V7h7V2.75a.75.75 0 0 1 1.5 0v10.5a.75.75 0 0 1-1.5 0V8.5h-7v4.75a.75.75 0 0 1-1.5 0V2.75A.75.75 0 0 1 3.75 2Z"/></svg>', title: "Heading (cycles H1–H6)", action: "heading" },
    h1: { icon: '<svg viewBox="0 0 16 16" width="16" height="16"><text x="1" y="13" font-size="13" font-weight="bold" font-family="sans-serif" fill="currentColor">H1</text></svg>', title: "Heading 1", action: "h1" },
    h2: { icon: '<svg viewBox="0 0 16 16" width="16" height="16"><text x="1" y="13" font-size="13" font-weight="bold" font-family="sans-serif" fill="currentColor">H2</text></svg>', title: "Heading 2", action: "h2" },
    h3: { icon: '<svg viewBox="0 0 16 16" width="16" height="16"><text x="1" y="13" font-size="13" font-weight="bold" font-family="sans-serif" fill="currentColor">H3</text></svg>', title: "Heading 3", action: "h3" },
    bold: { icon: '<svg viewBox="0 0 16 16" width="16" height="16"><path fill="currentColor" d="M4 2h4.5a3.501 3.501 0 0 1 2.852 5.53A3.499 3.499 0 0 1 9.5 14H4a1 1 0 0 1-1-1V3a1 1 0 0 1 1-1Zm1 7v3h4.5a1.5 1.5 0 0 0 0-3Zm3.5-2a1.5 1.5 0 0 0 0-3H5v3Z"/></svg>', title: "Bold (Ctrl+B)", action: "bold" },
    italic: { icon: '<svg viewBox="0 0 16 16" width="16" height="16"><path fill="currentColor" d="M6 2.75A.75.75 0 0 1 6.75 2h6.5a.75.75 0 0 1 0 1.5h-2.505l-3.858 9H9.25a.75.75 0 0 1 0 1.5h-6.5a.75.75 0 0 1 0-1.5h2.505l3.858-9H6.75A.75.75 0 0 1 6 2.75Z"/></svg>', title: "Italic (Ctrl+I)", action: "italic" },
    strikethrough: { icon: '<svg viewBox="0 0 16 16" width="16" height="16"><path fill="currentColor" d="M7.581 3.25c-2.036 0-2.778 1.082-2.778 1.786 0 .055.002.107.006.157a.75.75 0 0 1-1.496.114 3.56 3.56 0 0 1-.01-.271c0-1.832 1.75-3.286 4.278-3.286 1.418 0 2.721.58 3.514 1.093a.75.75 0 0 1-.814 1.26c-.64-.414-1.662-.853-2.7-.853Zm3.474 4.25h1.195a.75.75 0 0 1 0 1.5H3.75a.75.75 0 0 1 0-1.5h4.411c-.278-.09-.547-.194-.795-.31-.869-.409-1.56-.983-1.965-1.69H7.94c.263.395.678.722 1.204.983.551.272 1.21.467 1.911.517ZM8.012 12.75c1.648 0 2.86-.725 2.86-1.652 0-.107-.016-.222-.048-.339a.75.75 0 0 1 1.452-.376c.058.224.096.46.096.715 0 2.012-2.163 3.152-4.36 3.152-1.39 0-2.728-.473-3.614-1.236a.75.75 0 0 1 .985-1.13c.606.527 1.593.866 2.629.866Z"/></svg>', title: "Strikethrough", action: "strikethrough" },
    quote: { icon: '<svg viewBox="0 0 16 16" width="16" height="16"><path fill="currentColor" d="M1.75 2.5h12.5a.75.75 0 0 1 0 1.5H1.75a.75.75 0 0 1 0-1.5Zm4 5h8.5a.75.75 0 0 1 0 1.5h-8.5a.75.75 0 0 1 0-1.5Zm0 5h8.5a.75.75 0 0 1 0 1.5h-8.5a.75.75 0 0 1 0-1.5ZM2.5 7.75v6a.75.75 0 0 1-1.5 0v-6a.75.75 0 0 1 1.5 0Z"/></svg>', title: "Quote (Ctrl+Shift+.)", action: "quote" },
    code: { icon: '<svg viewBox="0 0 16 16" width="16" height="16"><path fill="currentColor" d="m11.28 3.22 4.25 4.25a.75.75 0 0 1 0 1.06l-4.25 4.25a.749.749 0 0 1-1.275-.326.749.749 0 0 1 .215-.734L13.94 8l-3.72-3.72a.749.749 0 0 1 .326-1.275.749.749 0 0 1 .734.215Zm-6.56 0a.751.751 0 0 1 1.042.018.751.751 0 0 1 .018 1.042L2.06 8l3.72 3.72a.749.749 0 0 1-.326 1.275.749.749 0 0 1-.734-.215L.47 8.53a.75.75 0 0 1 0-1.06Z"/></svg>', title: "Code (Ctrl+E)", action: "code" },
    link: { icon: '<svg viewBox="0 0 16 16" width="16" height="16"><path fill="currentColor" d="m7.775 3.275 1.25-1.25a3.5 3.5 0 1 1 4.95 4.95l-2.5 2.5a3.5 3.5 0 0 1-4.95 0 .751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018 1.998 1.998 0 0 0 2.83 0l2.5-2.5a2.002 2.002 0 0 0-2.83-2.83l-1.25 1.25a.751.751 0 0 1-1.042-.018.751.751 0 0 1-.018-1.042Zm-4.69 9.64a1.998 1.998 0 0 0 2.83 0l1.25-1.25a.751.751 0 0 1 1.042.018.751.751 0 0 1 .018 1.042l-1.25 1.25a3.5 3.5 0 1 1-4.95-4.95l2.5-2.5a3.5 3.5 0 0 1 4.95 0 .751.751 0 0 1-.018 1.042.751.751 0 0 1-1.042.018 1.998 1.998 0 0 0-2.83 0l-2.5 2.5a1.998 1.998 0 0 0 0 2.83Z"/></svg>', title: "Link (Ctrl+K)", action: "link" },
    image: { icon: '<svg viewBox="0 0 16 16" width="16" height="16"><path fill="currentColor" d="M16 13.25A1.75 1.75 0 0 1 14.25 15H1.75A1.75 1.75 0 0 1 0 13.25V2.75C0 1.784.784 1 1.75 1h12.5c.966 0 1.75.784 1.75 1.75ZM1.75 2.5a.25.25 0 0 0-.25.25v10.5c0 .138.112.25.25.25h.94l4.72-6.03a.75.75 0 0 1 1.18 0l4.72 6.03h.94a.25.25 0 0 0 .25-.25V2.75a.25.25 0 0 0-.25-.25ZM5.5 6a1.5 1.5 0 1 1-3.001-.001A1.5 1.5 0 0 1 5.5 6Z"/></svg>', title: "Image", action: "image" },
    "ordered-list": { icon: '<svg viewBox="0 0 16 16" width="16" height="16"><path fill="currentColor" d="M5 3.25a.75.75 0 0 1 .75-.75h8.5a.75.75 0 0 1 0 1.5h-8.5A.75.75 0 0 1 5 3.25Zm0 5a.75.75 0 0 1 .75-.75h8.5a.75.75 0 0 1 0 1.5h-8.5A.75.75 0 0 1 5 8.25Zm0 5a.75.75 0 0 1 .75-.75h8.5a.75.75 0 0 1 0 1.5h-8.5a.75.75 0 0 1-.75-.75ZM.924 10.32a.5.5 0 0 1-.851-.076l-.025-.059a.5.5 0 0 1 .09-.47l1.5-1.836a.5.5 0 0 1 .362-.179h.168a.5.5 0 0 1 .5.5v4a.5.5 0 0 1-1 0v-2.957l-.744.907Zm-.009-7.378a.5.5 0 0 1 .5-.442h.166a.5.5 0 0 1 .5.5v4a.5.5 0 1 1-1 0V4.18l-.747.912a.5.5 0 0 1-.768-.64l1.35-1.51Z"/></svg>', title: "Ordered List (Ctrl+Shift+7)", action: "ordered-list" },
    "unordered-list": { icon: '<svg viewBox="0 0 16 16" width="16" height="16"><path fill="currentColor" d="M5.75 2.5h8.5a.75.75 0 0 1 0 1.5h-8.5a.75.75 0 0 1 0-1.5Zm0 5h8.5a.75.75 0 0 1 0 1.5h-8.5a.75.75 0 0 1 0-1.5Zm0 5h8.5a.75.75 0 0 1 0 1.5h-8.5a.75.75 0 0 1 0-1.5ZM2 14a1 1 0 1 1 0-2 1 1 0 0 1 0 2Zm1-6a1 1 0 1 1-2 0 1 1 0 0 1 2 0ZM2 4a1 1 0 1 1 0-2 1 1 0 0 1 0 2Z"/></svg>', title: "Unordered List (Ctrl+Shift+8)", action: "unordered-list" },
    "task-list": { icon: '<svg viewBox="0 0 16 16" width="16" height="16"><path fill="currentColor" d="M2.5 1.75v11.5c0 .138.112.25.25.25h3.17a.75.75 0 0 1 0 1.5H2.75A1.75 1.75 0 0 1 1 13.25V1.75C1 .784 1.784 0 2.75 0h8.5C12.216 0 13 .784 13 1.75v7.736a.75.75 0 0 1-1.5 0V1.75a.25.25 0 0 0-.25-.25h-8.5a.25.25 0 0 0-.25.25Zm10.97 6.97 2 2a.75.75 0 0 1 0 1.06l-4.25 4.25a.75.75 0 0 1-1.06 0l-2-2a.75.75 0 1 1 1.06-1.06l1.47 1.47 3.72-3.72a.75.75 0 0 1 1.06 0ZM4.75 4h4.5a.75.75 0 0 1 0 1.5h-4.5a.75.75 0 0 1 0-1.5ZM4 7.75A.75.75 0 0 1 4.75 7h2.5a.75.75 0 0 1 0 1.5h-2.5A.75.75 0 0 1 4 7.75Z"/></svg>', title: "Task List", action: "task-list" },
    "horizontal-rule": { icon: '<svg viewBox="0 0 16 16" width="16" height="16"><path fill="currentColor" d="M0 7.75A.75.75 0 0 1 .75 7h14.5a.75.75 0 0 1 0 1.5H.75A.75.75 0 0 1 0 7.75Z"/></svg>', title: "Horizontal Rule", action: "horizontal-rule" },
    table: { icon: '<svg viewBox="0 0 16 16" width="16" height="16"><path fill="currentColor" d="M0 1.75C0 .784.784 0 1.75 0h12.5C15.216 0 16 .784 16 1.75v12.5A1.75 1.75 0 0 1 14.25 16H1.75A1.75 1.75 0 0 1 0 14.25ZM6.5 6.5v3h3v-3Zm3-1.5v-3h-3v3Zm1.5 1.5v3H14v-3Zm0-1.5V2h-3v3ZM6.5 11v3h3v-3Zm1.5-9.5v3H14v-3Zm-6 6h3v-3H2Zm0 1.5v3h3v-3Zm0-6v3h3V2Z"/></svg>', title: "Table", action: "table" },
    "code-block": { icon: '<svg viewBox="0 0 16 16" width="16" height="16"><path fill="currentColor" d="M0 1.75C0 .784.784 0 1.75 0h12.5C15.216 0 16 .784 16 1.75v12.5A1.75 1.75 0 0 1 14.25 16H1.75A1.75 1.75 0 0 1 0 14.25Zm1.75-.25a.25.25 0 0 0-.25.25v12.5c0 .138.112.25.25.25h12.5a.25.25 0 0 0 .25-.25V1.75a.25.25 0 0 0-.25-.25Zm7.47 3.97a.75.75 0 0 1 1.06 0l2.25 2.25a.75.75 0 0 1 0 1.06l-2.25 2.25a.749.749 0 0 1-1.275-.326.749.749 0 0 1 .215-.734L10.94 8 9.22 6.28a.75.75 0 0 1 0-1.06ZM6.78 6.28 5.06 8l1.72 1.72a.749.749 0 0 1-.326 1.275.749.749 0 0 1-.734-.215l-2.25-2.25a.75.75 0 0 1 0-1.06l2.25-2.25a.751.751 0 0 1 1.042.018.751.751 0 0 1 .018 1.042Z"/></svg>', title: "Code Block", action: "code-block" },
    highlight: { icon: '<svg viewBox="0 0 16 16" width="16" height="16"><path fill="currentColor" d="M3.5 11h2.044a1.5 1.5 0 0 0 1.06-.44L12.81 4.355a1.5 1.5 0 0 0 0-2.121l-.586-.586a1.5 1.5 0 0 0-2.122 0L3.94 7.854A1.5 1.5 0 0 0 3.5 8.914V11Zm1.5-2.086 5.5-5.5.586.586-5.5 5.5H5V8.914ZM1.75 13h12.5a.75.75 0 0 1 0 1.5H1.75a.75.75 0 0 1 0-1.5Z"/></svg>', title: "Highlight", action: "highlight" },
    "line-break": { icon: '<svg viewBox="0 0 16 16" width="16" height="16"><path fill="currentColor" d="M2.75 2a.75.75 0 0 0 0 1.5h10.5a.75.75 0 0 0 0-1.5Zm0 4a.75.75 0 0 0 0 1.5h10.5a2.75 2.75 0 0 1 0 5.5H5.81l1.97 1.97a.749.749 0 0 1-.326 1.275.749.749 0 0 1-.734-.215l-3.5-3.5a.75.75 0 0 1 0-1.06l3.5-3.5a.751.751 0 0 1 1.042.018.751.751 0 0 1 .018 1.042L5.81 11.5h7.44a1.25 1.25 0 0 0 0-2.5H2.75a.75.75 0 0 0 0-1.5Z"/></svg>', title: "Line Break", action: "line-break" },
    footnote: { icon: '<svg viewBox="0 0 16 16" width="16" height="16"><path fill="currentColor" d="M1 2.75C1 1.784 1.784 1 2.75 1h10.5c.966 0 1.75.784 1.75 1.75v10.5A1.75 1.75 0 0 1 13.25 15H2.75A1.75 1.75 0 0 1 1 13.25Zm1.75-.25a.25.25 0 0 0-.25.25v10.5c0 .138.112.25.25.25h10.5a.25.25 0 0 0 .25-.25V2.75a.25.25 0 0 0-.25-.25ZM5 5.75A.75.75 0 0 1 5.75 5h.5a.75.75 0 0 1 .75.75v3.5h.5a.75.75 0 0 1 0 1.5h-2a.75.75 0 0 1 0-1.5h.5v-2.5h-.25A.75.75 0 0 1 5 5.75Z"/></svg>', title: "Footnote", action: "footnote" },
    superscript: { icon: '<svg viewBox="0 0 16 16" width="16" height="16"><text x="0" y="13" font-size="12" font-weight="bold" font-family="sans-serif" fill="currentColor">X</text><text x="10" y="7" font-size="8" font-weight="bold" font-family="sans-serif" fill="currentColor">2</text></svg>', title: "Superscript", action: "superscript" },
    subscript: { icon: '<svg viewBox="0 0 16 16" width="16" height="16"><text x="0" y="11" font-size="12" font-weight="bold" font-family="sans-serif" fill="currentColor">X</text><text x="10" y="15" font-size="8" font-weight="bold" font-family="sans-serif" fill="currentColor">2</text></svg>', title: "Subscript", action: "subscript" },
    "details": { icon: '<svg viewBox="0 0 16 16" width="16" height="16"><path fill="currentColor" d="M0 1.75C0 .784.784 0 1.75 0h12.5C15.216 0 16 .784 16 1.75v12.5A1.75 1.75 0 0 1 14.25 16H1.75A1.75 1.75 0 0 1 0 14.25Zm1.75-.25a.25.25 0 0 0-.25.25v12.5c0 .138.112.25.25.25h12.5a.25.25 0 0 0 .25-.25V1.75a.25.25 0 0 0-.25-.25ZM8 10a.75.75 0 0 1-.53-.22l-2.5-2.5a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L8 8.19l1.97-1.97a.749.749 0 0 1 1.275.326.749.749 0 0 1-.215.734l-2.5 2.5A.75.75 0 0 1 8 10Z"/></svg>', title: "Collapsible Section", action: "details" },
    attach: { icon: '<svg viewBox="0 0 16 16" width="16" height="16"><path fill="currentColor" d="M12.212 3.02a1.753 1.753 0 0 0-2.478.003l-5.83 5.83a3.007 3.007 0 0 0-.88 2.127c0 .795.315 1.551.88 2.116a2.996 2.996 0 0 0 4.243 0l5.113-5.113a.75.75 0 0 1 1.06 1.06L9.207 14.16a4.506 4.506 0 0 1-6.364 0 4.496 4.496 0 0 1-1.318-3.187A4.506 4.506 0 0 1 2.843 7.79l5.83-5.83a3.003 3.003 0 0 1 4.243 0 3.005 3.005 0 0 1 0 4.243l-5.83 5.83a1.503 1.503 0 0 1-2.122 0 1.503 1.503 0 0 1 0-2.122l5.113-5.113a.75.75 0 0 1 1.06 1.06l-5.113 5.113a.003.003 0 0 0 0 .002.002.002 0 0 0 .002 0l5.83-5.83a1.503 1.503 0 0 0 0-2.123Z"/></svg>', title: "Attach File", action: "attach" },
    video: { icon: '<svg viewBox="0 0 16 16" width="16" height="16"><path fill="currentColor" d="M0 3.75C0 2.784.784 2 1.75 2h12.5c.966 0 1.75.784 1.75 1.75v8.5A1.75 1.75 0 0 1 14.25 14H1.75A1.75 1.75 0 0 1 0 12.25Zm1.75-.25a.25.25 0 0 0-.25.25v8.5c0 .138.112.25.25.25h12.5a.25.25 0 0 0 .25-.25v-8.5a.25.25 0 0 0-.25-.25ZM6 10.559V5.442a.25.25 0 0 1 .379-.215l4.264 2.559a.25.25 0 0 1 0 .428L6.379 10.773A.25.25 0 0 1 6 10.559Z"/></svg>', title: "Upload Video", action: "video" },
    document: { icon: '<svg viewBox="0 0 16 16" width="16" height="16"><path fill="currentColor" d="M3.75 1.5a.25.25 0 0 0-.25.25v12.5c0 .138.112.25.25.25h9.5a.25.25 0 0 0 .25-.25V6h-2.75A1.75 1.75 0 0 1 9 4.25V1.5Zm6.75.062V4.25c0 .138.112.25.25.25h2.688l-.011-.013-2.914-2.914-.013-.011ZM3.75 0h5.086c.464 0 .909.184 1.237.513l2.914 2.914c.329.328.513.773.513 1.237v9.586A1.75 1.75 0 0 1 11.75 16h-8A1.75 1.75 0 0 1 2 14.25V1.75C2 .784 2.784 0 3.75 0Z"/></svg>', title: "Upload Document", action: "document" },
    embed: { icon: '<svg viewBox="0 0 16 16" width="16" height="16"><path fill="currentColor" d="M0 2.75C0 1.784.784 1 1.75 1h12.5c.966 0 1.75.784 1.75 1.75v10.5A1.75 1.75 0 0 1 14.25 15H1.75A1.75 1.75 0 0 1 0 13.25Zm1.75-.25a.25.25 0 0 0-.25.25v10.5c0 .138.112.25.25.25h12.5a.25.25 0 0 0 .25-.25V2.75a.25.25 0 0 0-.25-.25ZM3.5 6.25a.75.75 0 0 1 .75-.75h7.5a.75.75 0 0 1 0 1.5h-7.5a.75.75 0 0 1-.75-.75Zm.75 2.25a.75.75 0 0 0 0 1.5h4.5a.75.75 0 0 0 0-1.5Z"/></svg>', title: "Embed (YouTube, etc.)", action: "embed" },
    undo: { icon: '<svg viewBox="0 0 16 16" width="16" height="16"><path fill="currentColor" d="M1.22 6.28a.749.749 0 0 1 0-1.06l3.5-3.5a.749.749 0 1 1 1.06 1.06L3.561 5h7.188a4.75 4.75 0 0 1 0 9.5H5.75a.75.75 0 0 1 0-1.5h4.999a3.25 3.25 0 0 0 0-6.5H3.561l2.22 2.22a.749.749 0 1 1-1.06 1.06Z"/></svg>', title: "Undo (Ctrl+Z)", action: "undo", align: "right" },
    redo: { icon: '<svg viewBox="0 0 16 16" width="16" height="16"><path fill="currentColor" d="M14.78 6.28a.749.749 0 0 0 0-1.06l-3.5-3.5a.749.749 0 1 0-1.06 1.06L12.439 5H5.25a4.75 4.75 0 0 0 0 9.5h4.999a.75.75 0 0 0 0-1.5H5.25a3.25 3.25 0 0 1 0-6.5h7.189l-2.22 2.22a.749.749 0 1 0 1.06 1.06Z"/></svg>', title: "Redo (Ctrl+Shift+Z)", action: "redo", align: "right" },
    fullscreen: { icon: '<svg viewBox="0 0 16 16" width="16" height="16"><path fill="currentColor" d="M1.75 10a.75.75 0 0 1 .75.75v2.5c0 .138.112.25.25.25h2.5a.75.75 0 0 1 0 1.5h-2.5A1.75 1.75 0 0 1 1 13.25v-2.5a.75.75 0 0 1 .75-.75Zm12.5 0a.75.75 0 0 1 .75.75v2.5A1.75 1.75 0 0 1 13.25 15h-2.5a.75.75 0 0 1 0-1.5h2.5a.25.25 0 0 0 .25-.25v-2.5a.75.75 0 0 1 .75-.75ZM2.75 1h2.5a.75.75 0 0 1 0 1.5h-2.5a.25.25 0 0 0-.25.25v2.5a.75.75 0 0 1-1.5 0v-2.5C1 1.784 1.784 1 2.75 1Zm10.5 0A1.75 1.75 0 0 1 15 2.75v2.5a.75.75 0 0 1-1.5 0v-2.5a.25.25 0 0 0-.25-.25h-2.5a.75.75 0 0 1 0-1.5Z"/></svg>', title: "Fullscreen", action: "fullscreen", align: "right" },
    separator: { type: "separator" },
  };

  // ---------------------------------------------------------------------------
  // 2. initEditor(container)
  // ---------------------------------------------------------------------------
  function initEditor(container) {
    let toolbarConfig;
    var configScript = container.querySelector(".md-editor-config");
    try {
      toolbarConfig = JSON.parse(configScript ? configScript.textContent : "[]");
    } catch (e) {
      toolbarConfig = Object.keys(TOOLBAR_BUTTONS);
    }
    if (!toolbarConfig.length) {
      toolbarConfig = Object.keys(TOOLBAR_BUTTONS);
    }
    const uploadUrl = container.dataset.uploadUrl || "";
    const finalizeUrl = container.dataset.finalizeUrl || "";

    const textarea = container.querySelector(".md-editor-textarea");

    // Undo/redo history
    var undoStack = [{ value: textarea.value || "", selStart: 0, selEnd: 0 }];
    var redoStack = [];
    var isUndoRedo = false;

    function pushUndo() {
      if (isUndoRedo) return;
      var state = { value: textarea.value, selStart: textarea.selectionStart, selEnd: textarea.selectionEnd };
      var last = undoStack[undoStack.length - 1];
      if (last && last.value === state.value) return;
      undoStack.push(state);
      if (undoStack.length > 100) undoStack.shift();
      redoStack.length = 0;
    }

    function performUndo() {
      if (undoStack.length <= 1) return;
      isUndoRedo = true;
      redoStack.push(undoStack.pop());
      var state = undoStack[undoStack.length - 1];
      textarea.value = state.value;
      textarea.selectionStart = state.selStart;
      textarea.selectionEnd = state.selEnd;
      triggerInput(textarea);
      isUndoRedo = false;
    }

    function performRedo() {
      if (!redoStack.length) return;
      isUndoRedo = true;
      var state = redoStack.pop();
      undoStack.push(state);
      textarea.value = state.value;
      textarea.selectionStart = state.selStart;
      textarea.selectionEnd = state.selEnd;
      triggerInput(textarea);
      isUndoRedo = false;
    }

    textarea.addEventListener("input", function () { pushUndo(); });

    // Autosave to localStorage
    var storageKey = "md-editor:" + window.location.pathname + ":" + (textarea.name || textarea.id || "default");
    var saveTimer = null;
    var autosaveEnabled = true;
    var autosaveCheckbox = container.querySelector(".md-editor-autosave-checkbox");
    var autosaveStatus = container.querySelector(".md-editor-footer-autosave-status");

    function formatTime(ts) {
      var d = new Date(ts);
      var h = d.getHours();
      var m = d.getMinutes();
      var ampm = h >= 12 ? "PM" : "AM";
      h = h % 12 || 12;
      return h + ":" + (m < 10 ? "0" : "") + m + " " + ampm;
    }

    function showStatus(text) {
      if (autosaveStatus) autosaveStatus.textContent = text;
    }

    function autosave() {
      if (!autosaveEnabled) return;
      showStatus("Saving\u2026");
      try {
        var now = Date.now();
        localStorage.setItem(storageKey, JSON.stringify({
          value: textarea.value,
          timestamp: now,
        }));
        showStatus("Saved at " + formatTime(now));
      } catch (e) {
        showStatus("Save failed");
      }
    }

    function scheduleAutosave() {
      if (!autosaveEnabled) return;
      if (saveTimer) clearTimeout(saveTimer);
      saveTimer = setTimeout(autosave, 500);
    }

    // Toggle autosave
    if (autosaveCheckbox) {
      autosaveCheckbox.checked = autosaveEnabled;
      autosaveCheckbox.addEventListener("change", function () {
        autosaveEnabled = this.checked;
        if (!autosaveEnabled) {
          if (saveTimer) clearTimeout(saveTimer);
          showStatus("");
        }
      });
    }

    // Restore draft on load
    try {
      var saved = JSON.parse(localStorage.getItem(storageKey));
      if (saved && saved.value) {
        var maxAge = 7 * 24 * 60 * 60 * 1000; // 7 days
        if (Date.now() - saved.timestamp < maxAge) {
          var serverValue = textarea.value || "";
          if (!serverValue || serverValue === textarea.defaultValue) {
            if (saved.value !== serverValue) {
              textarea.value = saved.value;
              undoStack[0] = { value: saved.value, selStart: 0, selEnd: 0 };
            }
          }
          showStatus("Draft from " + formatTime(saved.timestamp));
        } else {
          localStorage.removeItem(storageKey);
        }
      }
    } catch (e) { /* parse error or unavailable */ }

    textarea.addEventListener("input", scheduleAutosave);

    // Finalize uploads and clear draft on form submit
    var form = textarea.closest("form");
    if (form) {
      form.addEventListener("submit", function (e) {
        try { localStorage.removeItem(storageKey); } catch (ex) {}
        showStatus("");

        if (!finalizeUrl) return;

        // Check if content has any temp upload URLs
        var text = textarea.value;
        if (text.indexOf("/md-editor/tmp/") === -1) return;

        // Prevent default submit, finalize first
        e.preventDefault();
        fetch(finalizeUrl, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken(),
          },
          body: JSON.stringify({ text: text }),
        })
          .then(function (response) {
            if (!response.ok) throw new Error("Finalize failed");
            return response.json();
          })
          .then(function (data) {
            var replacements = data.replacements || {};
            var updated = textarea.value;
            for (var oldUrl in replacements) {
              updated = updated.split(oldUrl).join(replacements[oldUrl]);
            }
            textarea.value = updated;
            form.submit();
          })
          .catch(function () {
            // Submit anyway even if finalize fails
            form.submit();
          });
      });
    }

    // Fullscreen button in tabs bar
    var fullscreenBtn = container.querySelector(".md-editor-fullscreen-btn");
    if (fullscreenBtn) {
      fullscreenBtn.addEventListener("click", function () {
        container.classList.toggle("md-editor--fullscreen");
      });
    }

    const toolbar = container.querySelector(".md-editor-toolbar");
    const tabs = container.querySelectorAll(".md-editor-tab");
    const writePanels = container.querySelectorAll(".md-editor-write");
    const previewPanels = container.querySelectorAll(".md-editor-preview");
    const fileInput = container.querySelector(".md-editor-file-input");
    const footerUpload = container.querySelector(".md-editor-footer-upload");

    if (!textarea || !toolbar) return;

    // Build toolbar buttons
    let spacerInserted = false;
    toolbarConfig.forEach((name) => {
      const def = TOOLBAR_BUTTONS[name];
      if (!def) return;

      if (def.type === "separator") {
        const sep = document.createElement("span");
        sep.className = "md-editor-toolbar-separator";
        toolbar.appendChild(sep);
        return;
      }

      // Insert spacer before the first right-aligned button
      if (def.align === "right" && !spacerInserted) {
        const spacer = document.createElement("span");
        spacer.className = "md-editor-toolbar-spacer";
        spacer.style.flex = "1";
        toolbar.appendChild(spacer);
        spacerInserted = true;
      }

      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "md-editor-toolbar-btn";
      btn.setAttribute("aria-label", def.title);
      btn.dataset.action = def.action;
      btn.innerHTML = def.icon;
      if (def.style) btn.style.cssText = def.style;

      btn.addEventListener("click", function () {
        handleAction(def.action, textarea, container, fileInput, uploadUrl);
        textarea.focus();
      });

      toolbar.appendChild(btn);
    });

    // Wire tab switching (write / split / preview)
    var currentMode = "write";
    var splitInputHandler = null;
    var previewContent = container.querySelector(".md-editor-preview-content");

    function setMode(mode) {
      currentMode = mode;
      tabs.forEach((t) => t.classList.remove("md-editor-tab--active"));
      container.querySelector('[data-tab="' + mode + '"]').classList.add("md-editor-tab--active");
      container.classList.remove("md-editor--split");
      // Reset split panel widths
      writePanels.forEach(function (p) { p.style.width = ""; });
      previewPanels.forEach(function (p) { p.style.width = ""; });

      // Remove live-update listener from split mode
      if (splitInputHandler) {
        textarea.removeEventListener("input", splitInputHandler);
        splitInputHandler = null;
      }

      if (mode === "write") {
        writePanels.forEach((p) => { p.classList.remove("md-editor-panel--hidden"); p.classList.add("md-editor-panel--active"); });
        previewPanels.forEach((p) => { p.classList.add("md-editor-panel--hidden"); p.classList.remove("md-editor-panel--active"); });
        toolbar.style.display = "";
      } else if (mode === "preview") {
        writePanels.forEach((p) => { p.classList.add("md-editor-panel--hidden"); p.classList.remove("md-editor-panel--active"); });
        previewPanels.forEach((p) => { p.classList.remove("md-editor-panel--hidden"); p.classList.add("md-editor-panel--active"); });
        toolbar.style.display = "none";
        if (previewContent) renderPreview(textarea.value, previewContent);
      } else if (mode === "split") {
        container.classList.add("md-editor--split");
        writePanels.forEach((p) => { p.classList.remove("md-editor-panel--hidden"); p.classList.add("md-editor-panel--active"); });
        previewPanels.forEach((p) => { p.classList.remove("md-editor-panel--hidden"); p.classList.add("md-editor-panel--active"); });
        toolbar.style.display = "";
        if (previewContent) renderPreview(textarea.value, previewContent);

        // Live-update preview as user types
        splitInputHandler = function () {
          if (previewContent) renderPreview(textarea.value, previewContent);
        };
        textarea.addEventListener("input", splitInputHandler);
      }
    }

    tabs.forEach((tab) => {
      tab.addEventListener("click", function () {
        setMode(this.dataset.tab);
      });
    });

    // Wire draggable split divider
    var divider = container.querySelector(".md-editor-divider");
    if (divider) {
      var body = container.querySelector(".md-editor-body");
      var writePanel = container.querySelector(".md-editor-write");
      var previewPanel = container.querySelector(".md-editor-preview");

      divider.addEventListener("mousedown", startDrag);
      divider.addEventListener("touchstart", startDrag, { passive: false });

      function startDrag(e) {
        if (!container.classList.contains("md-editor--split")) return;
        e.preventDefault();
        divider.classList.add("md-editor-divider--dragging");
        var isTouch = e.type === "touchstart";

        function onMove(ev) {
          var clientX = isTouch ? ev.touches[0].clientX : ev.clientX;
          var rect = body.getBoundingClientRect();
          var offset = clientX - rect.left;
          var pct = Math.max(20, Math.min(80, (offset / rect.width) * 100));
          writePanel.style.width = "calc(" + pct + "% - 4.5px)";
          previewPanel.style.width = "calc(" + (100 - pct) + "% - 4.5px)";
        }

        function onUp() {
          divider.classList.remove("md-editor-divider--dragging");
          document.removeEventListener(isTouch ? "touchmove" : "mousemove", onMove);
          document.removeEventListener(isTouch ? "touchend" : "mouseup", onUp);
        }

        document.addEventListener(isTouch ? "touchmove" : "mousemove", onMove);
        document.addEventListener(isTouch ? "touchend" : "mouseup", onUp);
      }
    }

    // Wire keyboard shortcuts on textarea
    textarea.addEventListener("keydown", function (e) {
      const ctrl = e.ctrlKey || e.metaKey;

      if (ctrl && !e.shiftKey && e.key === "b") {
        e.preventDefault();
        handleAction("bold", textarea, container, fileInput, uploadUrl);
      } else if (ctrl && !e.shiftKey && e.key === "i") {
        e.preventDefault();
        handleAction("italic", textarea, container, fileInput, uploadUrl);
      } else if (ctrl && !e.shiftKey && e.key === "k") {
        e.preventDefault();
        handleAction("link", textarea, container, fileInput, uploadUrl);
      } else if (ctrl && !e.shiftKey && e.key === "e") {
        e.preventDefault();
        handleAction("code", textarea, container, fileInput, uploadUrl);
      } else if (ctrl && e.shiftKey && (e.key === ">" || e.key === ".")) {
        e.preventDefault();
        handleAction("quote", textarea, container, fileInput, uploadUrl);
      } else if (ctrl && e.shiftKey && e.key === "7") {
        e.preventDefault();
        handleAction("ordered-list", textarea, container, fileInput, uploadUrl);
      } else if (ctrl && e.shiftKey && e.key === "8") {
        e.preventDefault();
        handleAction("unordered-list", textarea, container, fileInput, uploadUrl);
      } else if (ctrl && !e.shiftKey && e.key === "z") {
        e.preventDefault();
        performUndo();
      } else if (ctrl && e.shiftKey && e.key === "z") {
        e.preventDefault();
        performRedo();
      } else if (e.key === "Escape") {
        if (container.classList.contains("md-editor--fullscreen")) {
          container.classList.remove("md-editor--fullscreen");
        }
      }
    });

    // Wire drag/drop file handling
    container.addEventListener("dragover", function (e) {
      e.preventDefault();
      container.classList.add("md-editor--dragover");
    });

    container.addEventListener("dragleave", function (e) {
      if (!container.contains(e.relatedTarget)) {
        container.classList.remove("md-editor--dragover");
      }
    });

    container.addEventListener("drop", function (e) {
      e.preventDefault();
      container.classList.remove("md-editor--dragover");
      if (e.dataTransfer && e.dataTransfer.files && e.dataTransfer.files.length > 0) {
        uploadFiles(e.dataTransfer.files, textarea, uploadUrl);
      }
    });

    // Wire paste file handling
    textarea.addEventListener("paste", function (e) {
      if (!e.clipboardData || !e.clipboardData.files || e.clipboardData.files.length === 0) return;
      const imageFiles = Array.from(e.clipboardData.files).filter((f) => f.type.startsWith("image/"));
      if (imageFiles.length > 0) {
        e.preventDefault();
        uploadFiles(imageFiles, textarea, uploadUrl);
      }
    });

    // Wire file input (hidden) change
    if (fileInput) {
      fileInput.addEventListener("change", function () {
        if (fileInput.files && fileInput.files.length > 0) {
          uploadFiles(fileInput.files, textarea, uploadUrl);
          fileInput.value = "";
        }
      });
    }

    // Wire footer upload click
    if (footerUpload && fileInput) {
      footerUpload.addEventListener("click", function () {
        fileInput.click();
      });
    }

  // ---------------------------------------------------------------------------
  // 3. handleAction
  // ---------------------------------------------------------------------------
  function handleAction(action, textarea, container, fileInput, uploadUrl) {
    switch (action) {
      case "heading":
        cycleHeading(textarea);
        break;
      case "h1":
        wrapLines(textarea, "# ");
        break;
      case "h2":
        wrapLines(textarea, "## ");
        break;
      case "h3":
        wrapLines(textarea, "### ");
        break;
      case "bold":
        wrapSelection(textarea, "**", "**");
        break;
      case "italic":
        wrapSelection(textarea, "_", "_");
        break;
      case "strikethrough":
        wrapSelection(textarea, "~~", "~~");
        break;
      case "quote":
        wrapLines(textarea, "> ");
        break;
      case "code":
        toggleCode(textarea);
        break;
      case "link":
        insertLink(textarea);
        break;
      case "image":
        insertImage(textarea);
        break;
      case "ordered-list":
        wrapLines(textarea, "1. ");
        break;
      case "unordered-list":
        wrapLines(textarea, "- ");
        break;
      case "task-list":
        wrapLines(textarea, "- [ ] ");
        break;
      case "horizontal-rule":
        insertAtCursor(textarea, "\n---\n");
        break;
      case "table":
        insertAtCursor(textarea, "\n| Header | Header |\n| ------ | ------ |\n| Cell   | Cell   |\n");
        break;
      case "code-block":
        insertAtCursor(textarea, "\n```\n\n```\n");
        break;
      case "highlight":
        wrapSelection(textarea, "==", "==");
        break;
      case "line-break":
        insertAtCursor(textarea, "  \n");
        break;
      case "footnote":
        insertFootnote(textarea);
        break;
      case "superscript":
        wrapSelection(textarea, "^", "^");
        break;
      case "subscript":
        wrapSelection(textarea, "~", "~");
        break;
      case "details":
        insertDetails(textarea);
        break;
      case "attach":
        if (fileInput) {
          fileInput.setAttribute("accept", "*/*");
          fileInput.click();
        }
        break;
      case "video":
        if (fileInput) {
          fileInput.setAttribute("accept", "video/*");
          fileInput.click();
        }
        break;
      case "document":
        if (fileInput) {
          fileInput.setAttribute("accept", ".pdf,.doc,.docx,.xls,.xlsx,.ppt,.pptx,.zip,.tar,.gz,.txt,.csv,.json");
          fileInput.click();
        }
        break;
      case "embed":
        insertEmbed(textarea);
        break;
      case "undo":
        performUndo();
        break;
      case "redo":
        performRedo();
        break;
      case "fullscreen":
        container.classList.toggle("md-editor--fullscreen");
        break;
      default:
        break;
    }
  }

  // ---------------------------------------------------------------------------
  // 4. Text manipulation helpers
  // ---------------------------------------------------------------------------

  function wrapSelection(textarea, before, after) {
    const start = textarea.selectionStart;
    const end = textarea.selectionEnd;
    const value = textarea.value;
    const selected = value.substring(start, end);

    // Toggle off if already wrapped
    const beforeLen = before.length;
    const afterLen = after.length;
    if (
      start >= beforeLen &&
      value.substring(start - beforeLen, start) === before &&
      value.substring(end, end + afterLen) === after
    ) {
      const newValue =
        value.substring(0, start - beforeLen) +
        selected +
        value.substring(end + afterLen);
      textarea.value = newValue;
      textarea.selectionStart = start - beforeLen;
      textarea.selectionEnd = end - beforeLen;
      triggerInput(textarea);
      return;
    }

    const text = selected || "text";
    const newValue = value.substring(0, start) + before + text + after + value.substring(end);
    textarea.value = newValue;

    if (selected) {
      textarea.selectionStart = start + beforeLen;
      textarea.selectionEnd = end + beforeLen;
    } else {
      textarea.selectionStart = start + beforeLen;
      textarea.selectionEnd = start + beforeLen + text.length;
    }
    triggerInput(textarea);
  }

  function wrapLines(textarea, prefix) {
    const start = textarea.selectionStart;
    const end = textarea.selectionEnd;
    const value = textarea.value;

    // Find the start of the first selected line
    const lineStart = value.lastIndexOf("\n", start - 1) + 1;
    // Find the end of the last selected line
    let lineEnd = value.indexOf("\n", end);
    if (lineEnd === -1) lineEnd = value.length;

    const selectedBlock = value.substring(lineStart, lineEnd);
    const lines = selectedBlock.split("\n");

    const allPrefixed = lines.every((line) => line.startsWith(prefix));

    let newBlock;
    if (allPrefixed) {
      // Toggle off
      newBlock = lines.map((line) => line.substring(prefix.length)).join("\n");
    } else {
      newBlock = lines.map((line) => (line.startsWith(prefix) ? line : prefix + line)).join("\n");
    }

    textarea.value = value.substring(0, lineStart) + newBlock + value.substring(lineEnd);
    textarea.selectionStart = lineStart;
    textarea.selectionEnd = lineStart + newBlock.length;
    triggerInput(textarea);
  }

  function toggleCode(textarea) {
    const start = textarea.selectionStart;
    const end = textarea.selectionEnd;
    const value = textarea.value;
    const selected = value.substring(start, end);

    if (selected.includes("\n")) {
      // Multi-line: use code fence
      const fence = "```";
      // Toggle off
      if (
        start >= fence.length + 1 &&
        value.substring(start - fence.length - 1, start) === fence + "\n" &&
        value.substring(end, end + fence.length + 1) === "\n" + fence
      ) {
        const newValue =
          value.substring(0, start - fence.length - 1) +
          selected +
          value.substring(end + fence.length + 1);
        textarea.value = newValue;
        textarea.selectionStart = start - fence.length - 1;
        textarea.selectionEnd = end - fence.length - 1;
      } else {
        const newValue =
          value.substring(0, start) + fence + "\n" + selected + "\n" + fence + value.substring(end);
        textarea.value = newValue;
        textarea.selectionStart = start + fence.length + 1;
        textarea.selectionEnd = end + fence.length + 1;
      }
    } else {
      // Single-line or no selection: inline backtick
      wrapSelection(textarea, "`", "`");
      return;
    }
    triggerInput(textarea);
  }

  function insertLink(textarea) {
    const start = textarea.selectionStart;
    const end = textarea.selectionEnd;
    const value = textarea.value;
    const selected = value.substring(start, end);

    if (selected) {
      // Selected text becomes link text
      const inserted = "[" + selected + "](url)";
      textarea.value = value.substring(0, start) + inserted + value.substring(end);
      // Place cursor on "url"
      const urlStart = start + selected.length + 3;
      textarea.selectionStart = urlStart;
      textarea.selectionEnd = urlStart + 3;
    } else {
      const inserted = "[text](url)";
      textarea.value = value.substring(0, start) + inserted + value.substring(end);
      // Select "text"
      textarea.selectionStart = start + 1;
      textarea.selectionEnd = start + 5;
    }
    triggerInput(textarea);
  }

  function insertImage(textarea) {
    const start = textarea.selectionStart;
    const end = textarea.selectionEnd;
    const value = textarea.value;
    const selected = value.substring(start, end);

    if (selected) {
      // Selected text becomes alt text
      const inserted = "![" + selected + "](url)";
      textarea.value = value.substring(0, start) + inserted + value.substring(end);
      // Place cursor on "url"
      const urlStart = start + selected.length + 4;
      textarea.selectionStart = urlStart;
      textarea.selectionEnd = urlStart + 3;
    } else {
      const inserted = "![alt](url)";
      textarea.value = value.substring(0, start) + inserted + value.substring(end);
      // Select "alt"
      textarea.selectionStart = start + 2;
      textarea.selectionEnd = start + 5;
    }
    triggerInput(textarea);
  }

  function cycleHeading(textarea) {
    var start = textarea.selectionStart;
    var value = textarea.value;
    var lineStart = value.lastIndexOf("\n", start - 1) + 1;
    var lineEnd = value.indexOf("\n", start);
    if (lineEnd === -1) lineEnd = value.length;
    var line = value.substring(lineStart, lineEnd);

    var match = line.match(/^(#{1,6})\s/);
    if (match) {
      var level = match[1].length;
      if (level >= 6) {
        // Remove heading
        var newLine = line.replace(/^#{1,6}\s/, "");
        textarea.value = value.substring(0, lineStart) + newLine + value.substring(lineEnd);
      } else {
        // Increase level
        var newLine = "#" + line;
        textarea.value = value.substring(0, lineStart) + newLine + value.substring(lineEnd);
      }
    } else {
      // Add H1
      var newLine = "# " + line;
      textarea.value = value.substring(0, lineStart) + newLine + value.substring(lineEnd);
    }
    textarea.selectionStart = lineStart;
    textarea.selectionEnd = lineStart;
    triggerInput(textarea);
  }

  function insertFootnote(textarea) {
    var start = textarea.selectionStart;
    var value = textarea.value;
    // Find existing footnotes to auto-number
    var matches = value.match(/\[\^\d+\]/g);
    var num = matches ? matches.length / 2 + 1 : 1;
    var ref = "[^" + num + "]";
    var def = "\n\n" + ref + ": ";
    // Insert reference at cursor
    textarea.value = value.substring(0, start) + ref + value.substring(start) + def;
    textarea.selectionStart = start + ref.length + def.length;
    textarea.selectionEnd = textarea.selectionStart;
    triggerInput(textarea);
  }

  function insertDetails(textarea) {
    var start = textarea.selectionStart;
    var end = textarea.selectionEnd;
    var value = textarea.value;
    var selected = value.substring(start, end) || "Content here";
    var block = "\n<details>\n<summary>Click to expand</summary>\n\n" + selected + "\n\n</details>\n";
    textarea.value = value.substring(0, start) + block + value.substring(end);
    // Select "Click to expand"
    var summaryStart = start + "\n<details>\n<summary>".length;
    textarea.selectionStart = summaryStart;
    textarea.selectionEnd = summaryStart + "Click to expand".length;
    triggerInput(textarea);
  }

  function insertEmbed(textarea) {
    var input = prompt("Paste a URL or embed code (YouTube, Vimeo, CodePen, etc.):");
    if (!input) return;
    input = input.trim();

    var embedHtml = "";

    // User pasted an <iframe> embed code directly — use it as-is (sanitized)
    if (input.toLowerCase().indexOf("<iframe") !== -1) {
      embedHtml = sanitizeHtml(input);
    } else {
      var youtubeMatch = input.match(/(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([\w-]+)/);
      var vimeoMatch = input.match(/vimeo\.com\/(\d+)/);
      var codepenMatch = input.match(/codepen\.io\/([\w-]+)\/pen\/([\w-]+)/);

      if (youtubeMatch) {
        embedHtml = '<iframe width="100%" height="400" src="https://www.youtube.com/embed/' + escapeHtml(youtubeMatch[1]) + '" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>';
      } else if (vimeoMatch) {
        embedHtml = '<iframe width="100%" height="400" src="https://player.vimeo.com/video/' + escapeHtml(vimeoMatch[1]) + '" frameborder="0" allow="autoplay; fullscreen; picture-in-picture" allowfullscreen></iframe>';
      } else if (codepenMatch) {
        embedHtml = '<iframe width="100%" height="400" src="https://codepen.io/' + escapeHtml(codepenMatch[1]) + '/embed/' + escapeHtml(codepenMatch[2]) + '?default-tab=result" frameborder="0"></iframe>';
      } else {
        embedHtml = '<iframe width="100%" height="400" src="' + escapeHtml(input) + '" frameborder="0"></iframe>';
      }
    }

    insertAtCursor(textarea, "\n" + embedHtml + "\n");
  }

  function showToast(container, message, type) {
    var toast = document.createElement("div");
    toast.className = "md-editor-toast md-editor-toast--" + (type || "error");
    toast.textContent = message;
    container.appendChild(toast);
    setTimeout(function () {
      toast.classList.add("md-editor-toast--fade");
      setTimeout(function () { toast.remove(); }, 300);
    }, 4000);
  }

  function insertAtCursor(textarea, text) {
    const start = textarea.selectionStart;
    const end = textarea.selectionEnd;
    const value = textarea.value;
    textarea.value = value.substring(0, start) + text + value.substring(end);
    textarea.selectionStart = start + text.length;
    textarea.selectionEnd = start + text.length;
    triggerInput(textarea);
  }

  function triggerInput(textarea) {
    textarea.dispatchEvent(new Event("input", { bubbles: true }));
  }

  // ---------------------------------------------------------------------------
  // 5. Initialize markdown-it with highlight.js
  // ---------------------------------------------------------------------------
  var md = null;
  if (typeof markdownit !== "undefined") {
    var mdOptions = { html: true, linkify: true, typographer: true };
    if (typeof hljs !== "undefined") {
      mdOptions.highlight = function (code, lang) {
        if (lang && hljs.getLanguage(lang)) {
          return hljs.highlight(code, { language: lang }).value;
        }
        return hljs.highlightAuto(code).value;
      };
    }
    md = markdownit(mdOptions);

    // Load bundled plugins
    if (typeof markdownitMark !== "undefined") md.use(markdownitMark);
    if (typeof markdownitSub !== "undefined") md.use(markdownitSub);
    if (typeof markdownitSup !== "undefined") md.use(markdownitSup);
    if (typeof markdownitTaskLists !== "undefined") md.use(markdownitTaskLists);
  }

  // ---------------------------------------------------------------------------
  // 6. renderPreview (client-side only)
  // ---------------------------------------------------------------------------
  // Client-side HTML sanitizer for preview
  var SAFE_TAGS = /^(p|br|hr|h[1-6]|em|strong|del|s|mark|sub|sup|ul|ol|li|a|img|video|source|pre|code|blockquote|table|thead|tbody|tr|th|td|details|summary|input|div|span)$/i;
  var DANGEROUS_TAG_RE = /<(script|style|object|embed|form|textarea|select|button)[^>]*>[\s\S]*?<\/\1>/gi;
  var EVENT_ATTR_RE = /\s+on\w+\s*=\s*("[^"]*"|'[^']*'|[^\s>]*)/gi;
  var JS_URL_RE = /(href|src)\s*=\s*["']?\s*javascript:/gi;

  function sanitizeHtml(html) {
    html = html.replace(DANGEROUS_TAG_RE, "");
    html = html.replace(EVENT_ATTR_RE, "");
    html = html.replace(JS_URL_RE, '$1=""');
    return html;
  }

  function renderPreview(markdown, previewEl) {
    if (!markdown) {
      previewEl.innerHTML = "<p style='color:var(--md-text-muted)'>Nothing to preview</p>";
      return;
    }

    if (md) {
      try {
        previewEl.innerHTML = sanitizeHtml(md.render(markdown)); // eslint-disable-line
      } catch (e) {
        previewEl.textContent = markdown;
      }
    } else {
      previewEl.textContent = markdown;
    }
  }

  // ---------------------------------------------------------------------------
  // 6. uploadFiles
  // ---------------------------------------------------------------------------
  function uploadFiles(files, textarea, uploadUrl) {
    if (!uploadUrl) return;

    Array.from(files).forEach(function (file) {
      const placeholder = "Uploading " + file.name + "...";
      insertAtCursor(textarea, placeholder);

      const formData = new FormData();
      formData.append("file", file);

      fetch(uploadUrl, {
        method: "POST",
        headers: {
          "X-CSRFToken": getCSRFToken(),
        },
        body: formData,
      })
        .then(function (response) {
          return response.json().then(function (data) {
            if (!response.ok) {
              var errMsg = data.error || "Upload failed";
              throw new Error(errMsg);
            }
            return data;
          });
        })
        .then(function (data) {
          const url = data.url || data.file_url || data.location || "";
          const name = data.name || file.name;
          const contentType = data.type || file.type || "";
          var replacement;
          if (contentType.startsWith("image/")) {
            replacement = "![" + name + "](" + url + ")";
          } else if (contentType.startsWith("video/")) {
            var autoplay = confirm("Autoplay this video?");
            replacement = '<video src="' + escapeHtml(url) + '"' + (autoplay ? " autoplay muted loop" : "") + ' controls controlslist="nodownload noplaybackrate" disablepictureinpicture width="100%">' + escapeHtml(name) + "</video>";
          } else {
            replacement = "[" + name + "](" + url + ")";
          }
          replacePlaceholder(textarea, placeholder, replacement);
        })
        .catch(function (err) {
          replacePlaceholder(textarea, placeholder, "");
          showToast(container, "Upload failed: " + err.message, "error");
        });
    });
  }

  function replacePlaceholder(textarea, placeholder, replacement) {
    const idx = textarea.value.indexOf(placeholder);
    if (idx === -1) return;
    textarea.value =
      textarea.value.substring(0, idx) +
      replacement +
      textarea.value.substring(idx + placeholder.length);
    triggerInput(textarea);
  }

  // ---------------------------------------------------------------------------
  // 7. escapeHtml
  // ---------------------------------------------------------------------------
  function escapeHtml(str) {
    return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  }

  // ---------------------------------------------------------------------------
  // 8. getCSRFToken
  // ---------------------------------------------------------------------------
  function getCSRFToken() {
    // Try cookie
    const cookieMatch = document.cookie.match(/(?:^|;\s*)csrftoken=([^;]+)/);
    if (cookieMatch) return decodeURIComponent(cookieMatch[1]);

    // Try hidden input
    const input = document.querySelector("[name=csrfmiddlewaretoken]");
    if (input) return input.value;

    // Try meta tag
    const meta = document.querySelector("meta[name=csrf-token]");
    if (meta) return meta.getAttribute("content") || "";

    return "";
  }

  } // end initEditor

  // ---------------------------------------------------------------------------
  // 8. initAll
  // ---------------------------------------------------------------------------
  function initAll() {
    document.querySelectorAll(".md-editor").forEach(initEditor);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initAll);
  } else {
    initAll();
  }
})();

-- mermaid.lua
--
-- Render each ```mermaid fenced block to SVG with mermaid-cli (mmdc) and
-- replace the block with an image. Each diagram gets a unique SVG id so the
-- inlined stylesheets of several diagrams cannot collide in one HTML page.
--
-- Environment:
--   MERMAID_OUT_DIR  directory for .mmd sources and .svg outputs (required)
--   MERMAID_BG       background color passed to mmdc (default #ffffff, the page color)

local out_dir = os.getenv("MERMAID_OUT_DIR")
local background = os.getenv("MERMAID_BG") or "#ffffff"
local counter = 0

function CodeBlock(block)
  if not block.classes:includes("mermaid") then
    return nil
  end
  if not out_dir then
    error("MERMAID_OUT_DIR is not set")
  end
  counter = counter + 1
  local name = string.format("diagram-%02d", counter)
  local src = out_dir .. "/" .. name .. ".mmd"
  local svg = out_dir .. "/" .. name .. ".svg"
  local f = assert(io.open(src, "w"))
  f:write(block.text)
  f:close()
  pandoc.pipe("mmdc", {"-q", "-i", src, "-o", svg, "-b", background, "-I", name, "-w", "1200"}, "")
  local img = pandoc.Image({}, svg, "", {class = "diagram"})
  return pandoc.Para({img})
end

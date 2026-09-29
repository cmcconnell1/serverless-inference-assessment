-- links.lua
--
-- Make repository-relative links work inside a single PDF.
--   docs/NN-*.md          -> #ch-NN (chapter anchor from assemble.py), or the
--                            link text alone when external-chapters is set
--   evidence/derived/X.md -> #ev-X when X is in the evidence appendix
--   any other local path  -> plain text plus the repository path
-- Headings titled "Sources" are excluded from the table of contents.
--
-- Metadata:
--   evidence-included  list of derived table names present in the appendix
--   external-chapters  true when the chapters are not in this PDF (the brief)

local included = {}
local external_chapters = false

local function collect(meta)
  local list = meta["evidence-included"]
  if list then
    for _, item in ipairs(list) do
      included[pandoc.utils.stringify(item)] = true
    end
  end
  external_chapters = meta["external-chapters"] == true
end

local function rewrite(link)
  local target = link.target
  if target:match("^%a[%w+.-]*:") or target:match("^#") then
    return nil
  end
  local path = target:gsub("#.*$", "")
  local base = path:match("([^/]+)$") or path
  local chapter = base:match("^(%d%d%a?)%-.*%.md$")
  if chapter and path:match("docs/") and external_chapters then
    return link.content
  end
  if chapter then
    link.target = "#ch-" .. chapter
    return link
  end
  local ev = path:match("evidence/derived/([%w%-]+)%.md$")
  if ev and included[ev] then
    link.target = "#ev-" .. ev
    return link
  end
  local repo_path = path:gsub("^%.%./", ""):gsub("^%./", "")
  local text = pandoc.utils.stringify(link.content):gsub("/$", "")
  local bare = repo_path:gsub("/$", "")
  if text == bare or text:find(bare, 1, true) then
    return pandoc.Code(repo_path)
  end
  local out = link.content:clone()
  out:insert(pandoc.Space())
  out:insert(pandoc.Str("(repository:"))
  out:insert(pandoc.Space())
  out:insert(pandoc.Code(repo_path))
  out:insert(pandoc.Str(")"))
  return out
end

local function unlist_sources(header)
  if pandoc.utils.stringify(header.content) == "Sources" then
    header.classes:insert("unlisted")
    return header
  end
  return nil
end

return {
  {Meta = collect},
  {Link = rewrite, Header = unlist_sources},
}

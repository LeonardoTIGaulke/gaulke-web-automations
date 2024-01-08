const rulesTag_ToPost = new Array();
function selectTag(e){
    // e.style.display = "none"
    // e.remove();
    console.log(e);
    var contentTag = e.querySelector("span").textContent.trim();
    console.log(contentTag)
    document.querySelector(".content-filter-tags").appendChild(e);
    rulesTag_ToPost.push(contentTag);
    console.log(rulesTag_ToPost);
}


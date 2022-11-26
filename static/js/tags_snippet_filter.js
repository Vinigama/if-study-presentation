$(document).ready(function(){
    ul = document.querySelector("#tags");
    input = document.querySelector("#input_tag");
    tagNumb = document.querySelector(".details span");

    maxTags = 10;
    tags = Array.isArray(tags) ? tags : [];
    countTags();
    createTag();

    input.addEventListener("keyup", addTag);

    $.prototype.getTagsValues = getTagsValues;

    $(window).keydown(function(event){
        if(event.keyCode == 13) {
          event.preventDefault();
          return false;
        }
      });
})
   
    function countTags(){
        // input.focus();
        // tagNumb.innerText = maxTags - tags.length;
    }
    
    function createTag(){
        ul.querySelectorAll("li").forEach(li => li.remove());
        tags.slice().reverse().forEach(tag =>{
            let liTag = `<li>${tag}<input type="checkbox" class="no-box" name="tags" value="${tag}" checked/><i class="fas fa-times" onclick="remove(this, '${tag}')"></i></li>`;
            ul.insertAdjacentHTML("afterbegin", liTag);
        });
        countTags();
    }

    function remove(element, tag){
        let index  = tags.indexOf(tag); 
        tags = [...tags.slice(0, index), ...tags.slice(index + 1)];
        element.parentElement.remove();
        countTags();
    }
    
    function addTag(e){
        if(e.key == "Enter"){
            let tag = e.target.value.replace(/\s+/g, ' ');
            if(tag.length > 0 && !tags.includes(tag)){
                if(tags.length < 10){
                    tag.split(',').forEach(tag => {
                        tags.push(tag);
                        createTag();
                    });
                }
            }
            e.target.value = "";
        }
    }

    
    function getTagsValues(){
        let tags = []
        $(this).children('li').each(function() {
            tags.push($(this).text())
        })
        return tags
    }
    
// const removeBtn = document.querySelector(".details button");
// removeBtn.addEventListener("click", () =>{
//     tags.length = 0;
//     ul.querySelectorAll("li").forEach(li => li.remove());
//     countTags();
// });

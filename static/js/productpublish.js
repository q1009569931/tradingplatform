//图片预览
// var FReader_img = new FileReader()
// var FReader_img_sub = new FileReader()

// FReader_img.onload = function(e){
//     document.getElementById("showimg").src = e.target.result;
// }
// FReader_img_sub.onload = function(e){
//     document.getElementById("showimg_sub").src = e.target.result;
// }

// var f = function(FReader, id){
//     var file_img = document.getElementById(id).files;
//     if (file_img.length === 0) { return; }
//     FReader.readAsDataURL(file_img[0]);
// }

// document.getElementById("addimg").onchange = function(){ f(FReader_img, "addimg") };
// document.getElementById("addimg_sub").onchange = function(){ f(FReader_img_sub
//     , "addimg_sub") };

function handleFileSelect(evt, id) {
var files = evt.target.files; // FileList object

// Loop through the FileList and render image files as thumbnails.
for (var i = 0, f; f = files[i]; i++) {

  if (i>=3) {
  	break;
  }
  // Only process image files.
  if (!f.type.match('image.*')) {
    continue;
  }

  var reader = new FileReader();

  // Closure to capture the file information.
  reader.onload = (function(theFile) {
    return function(e) {
      // Render thumbnail.
      var span = document.createElement('span');
      span.innerHTML = ['<img class="thumb" src="', e.target.result,
                        '" title="', decodeURI(theFile.name), '"/>'].join('');
      document.getElementById(id).insertBefore(span, null);
    };
  })(f);

  // Read in the image file as a data URL.
  reader.readAsDataURL(f);
}
}

document.getElementById('main_image').addEventListener('change', function(e) {handleFileSelect(e, 'mainlist');}, false);
document.getElementById('sub_image').addEventListener('change', function(e) {handleFileSelect(e, 'sublist');}, false);

/* needed to send ajax requests
 * https://docs.djangoproject.com/en/dev/ref/contrib/csrf/#ref-contrib-csrf */
$(document).ajaxSend(function(event, xhr, settings) {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = $.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(
                        cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    function sameOrigin(url) {
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var srOrigin = '//' + host;
        var origin = protocol + srOrigin;
        // allow absolute or scheme relative URLs to same origin
        return (url == origin ||
            url.slice(0, origin.length + 1) == origin + '/') ||
            (url == srOrigin ||
                url.slice(0, srOrigin.length + 1) == srOrigin + '/') ||
    // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }
    function safeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
        xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
    }
});


function makeArray(len, value) {
  return new Array(len).fill(value);
}


function getShortestColumnIndex(colArray) {
  return colArray.indexOf(Math.min(...colArray));
}


function getLeftPosition(colIndex, numColumns) {
  var gutter = 12;
  var pinWidth = 236;
  if (colIndex == 0){
    return gutter;
  }else{
    return gutter * (colIndex + 1) + pinWidth * colIndex;
  }
}


function getTopPosition(colIndex, colArray){
    return colArray[colIndex];
}


function updateColArray(colIndex, colArray, pinHeight){
  colArray[colIndex] += (pinHeight + 120);
  return colArray;
}


var screenWidth = $(window).width();
var gutter = 12;
var numColumns = Math.floor(screenWidth / (236 + gutter));
// initialize height of all page columns to zero
var colArray = makeArray(numColumns, 0);


function renderPins(resp){
  Object.values(resp["data"]).map(function(v) {
      return $(`<div data-height="${v.img_height}" style="padding:15px;position:absolute;">
        <img style="border-radius:10px;" width=236 src="${v.img_url}">
        <div style="min-height:13px;width: 236px;position:relative;padding-left:8px;padding-right:8px;">
            <div style="position:relative;max-width:145px;">
                <p style="max-width: 180px;margin-top:0;padding:0;max-height:60px;overflow:hidden;text-overflow:ellipsis;">${v.description}
                </p>
            </div>
            <div style="position:absolute;right:0;top:1px;z-index:3;">
                <p style="color:#a7a7a7">${v.repin_count} repins
                </p>
            </div>
        </div>
        <div style="display:flex;position:relative;-webkit-box-align:center;padding-left:8px;padding-right:8px;margin-top:4px;"
        >
            <div style="padding:0;display:flex;">
                <a href="pinterest.com/${v.pinner.username}" page style="-webkit-box-align: center;text-decoration:none">
                    <div style="height:24px;width:24px;margin-right:8px;">
                        <img src="${v.pinner.img_url}" style="height:24px;width:24px;border-radius:50%;position:static;">
                    </div>
                    <div>
                        <div style="display:block;overflow:hidden; text-overflow:ellipsis;">
                    ${v.pinner.username}</div>
                        <div style="display:block;overflow:hidden; text-overflow:ellipsis;">
                    ${v.boards.name}</div>         
                    </div>

                </a>
             </div>
        </div>
      </div>`)

  }).forEach(function(v) {
      var imageHeight = v.data("height");
      var pinHeight = imageHeight + 24 + 24;
      var columnIdx = getShortestColumnIndex(colArray);
      var left = getLeftPosition(columnIdx, numColumns);
      var top = getTopPosition(columnIdx, colArray);
      colArray = updateColArray(columnIdx, colArray, pinHeight);
      v.css("top", top.toString() + "px");
      v.css("left", left.toString() + "px");
      v.css("width", "236px");
      v.css("height", "100%");
      $('#pin-container').append(v);
  });
}


function getMorePinsOnScroll(){
  $(window).scroll(function() {
      if($(window).scrollTop() == $(document).height() - $(window).height()) {
        $.ajax({
            url: '/pins/get_more_pins/',
            type: 'POST',
            data: {},
            success: function(resp) {
                if (resp.status == 'ok'){
                    renderPins(resp);
                }
            }
         });
      }
  });
}


function createPin() {
    var pin_data = {
      'title':$('#title').val(),
      'description': $('#description').val(),
      'full_name': $('#full_name').val(),
      'board_name': $('#board_name').val(),
      'img_url':$('#img_url').val(),
    };
    $.ajax({
        url: '/pins/create_new_pin/',
        type: 'POST',
        data: pin_data,
        success: function(resp) {
            if (resp.status == 'ok'){
                renderPins(resp);
                window.alert('Your pin was created and added to the bottom of the loaded pins!');
            }
        }
     });
};


function createPinOnSubmit(){
  $('#create-pin-form').submit(function(event){
      event.preventDefault();
      createPin();
      $('#create-pin-modal').modal('hide');

  });
}


function fetchAllInitialPins(){
  $.ajax({
      url: '/pins/get_all_pins/',
      type: 'POST',
      data: {},
      success: function(resp) {
          if (resp.status == 'ok'){
              renderPins(resp);
          }
      }
   });
}


window.onload = function () {
  createPinOnSubmit();
  getMorePinsOnScroll();
  fetchAllInitialPins();
};
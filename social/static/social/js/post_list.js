// container 사이즈 조절 및 DOM 이벤트 등록을 위한 위한 ready script
$(document).ready(function(){
    var filter = new Array('win16', 'win32', 'win64', 'mac');
    if(navigator.platform){
        if(0 > filter.indexOf(navigator.platform.toLowerCase())){ // mobile 이면
            $('#post_main_container').attr('class', 'container mt-4 text-center text-dark');
        }else{ // pc 면
            $('#post_main_container').attr('class', 'container mt-4 text-center text-dark w-50');
        }
    }


      // 무한 스크롤 - 스크롤 event
    $(window).scroll(function(){
        var scrollTop = $(window).scrollTop();
        var documentHeight = $(document).height();
        var windowHeight = $(window).height();

        if( scrollTop >= documentHeight - windowHeight){
            var timer;
            if (!timer) {
                timer = setTimeout(function(){
                    timer = null;
                    var page = $('#page').val();
                    callMorePostAjax(page);
                    $('#page').val(parseInt(page)+1);
                }, 500);
            }
        }
    });


    // input file에 파일 선택시 label의 값을 file name으로 바꾸는 script
    $('#inputGroupFile01').change(function(){
        file_name = $('#inputGroupFile01')[0].files[0].name;
        $('#inputGroupFile01_label').html(file_name);
    });


    // image 클릭 시 modal이 show일 때 동작하는 script
    $('#imageModal').on('show.bs.modal', function(e){
        var test = $(e.relatedTarget).data('origin');
        console.log(test);
        $('#origin_image').attr('src', test);
    });


    // 화면 맨위로 올리는 script
    $("#move_to_top").click(function() {
        $('html, body').animate({
            scrollTop : 0
        }, 500);
        return false;
    });
});


// post update 요청하는 script
function postUpdate(clicked_item, post_id){
    var content = $(clicked_item).parents('div').find('#id_content_'+post_id);
    var content_value = $(clicked_item).parents('div').find('#id_content_'+post_id).val();
    $.ajax({
        url : '/social/update/', //'{% url 'social:postUpdate' %}',
        type : 'POST',
        data : {
                post_id: post_id,
                content: content_value,
                csrfmiddlewaretoken: csrftoken // ytbl/base.js 에서 csrf token 가져옴
                },
        success: function(data){
            alert('수정 완료!');
            location.reload();
        }, error: function(err, status){
            alert('서버 응답 실패!');
        }
    });
}


// post update로 변경하는 script
function setPostToUpdateForm(clicked_item, post_id){
    var post_content = $(clicked_item).parents('div').find('#post_'+post_id+'_content');
    var input_textarea = '<div class="card-text mb-1">'+
                                '<textarea name="content" id="id_content_'+post_id+'" rows="8" placeholder="내용을 적어주세요." style="resize:none;">'+post_content.text()+'</textarea>'+
                            '</div>'+
                            '<div class="card-text text-right">'+
                                '<button class="btn btn-secondary mr-2" onclick="location.reload();">취소</button>'+
                                '<button class="btn btn-primary" onclick="javascript:postUpdate(this, '+post_id+');">수정</button>'+
                            '</div>'
    $('#dropdown_btn_'+post_id).hide(); // 드롭다운 숨김
    post_content.html(input_textarea);
}


// post 댓글 icon 채우기 및 마지막 댓글 불러오는 script
function fillCommentIcon(target_object, post_id){
    var object = $(target_object).children();
    var filled_icon = '<path fill-rule="evenodd" d="M16 8c0 3.866-3.582 7-8 7a9.06 9.06 0 0 1-2.347-.306c-.584.296-1.925.864-4.181 1.234-.2.032-.352-.176-.273-.362.354-.836.674-1.95.77-2.966C.744 11.37 0 9.76 0 8c0-3.866 3.582-7 8-7s8 3.134 8 7zM5 8a1 1 0 1 1-2 0 1 1 0 0 1 2 0zm4 0a1 1 0 1 1-2 0 1 1 0 0 1 2 0zm3 1a1 1 0 1 0 0-2 1 1 0 0 0 0 2z"/>'
    var non_filled_icon = '<path fill-rule="evenodd" d="M2.678 11.894a1 1 0 0 1 .287.801 10.97 10.97 0 0 1-.398 2c1.395-.323 2.247-.697 2.634-.893a1 1 0 0 1 .71-.074A8.06 8.06 0 0 0 8 14c3.996 0 7-2.807 7-6 0-3.192-3.004-6-7-6S1 4.808 1 8c0 1.468.617 2.83 1.678 3.894zm-.493 3.905a21.682 21.682 0 0 1-.713.129c-.2.032-.352-.176-.273-.362a9.68 9.68 0 0 0 .244-.637l.003-.01c.248-.72.45-1.548.524-2.319C.743 11.37 0 9.76 0 8c0-3.866 3.582-7 8-7s8 3.134 8 7-3.582 7-8 7a9.06 9.06 0 0 1-2.347-.306c-.52.263-1.639.742-3.468 1.105z"/>'+
                            '<path d="M5 8a1 1 0 1 1-2 0 1 1 0 0 1 2 0zm4 0a1 1 0 1 1-2 0 1 1 0 0 1 2 0zm4 0a1 1 0 1 1-2 0 1 1 0 0 1 2 0z"/>'

    if ($('#collapseExample_'+post_id).is(':hidden')){  // 댓글창이 아직 안열렸다면
        object.html(filled_icon);
        getLastComment(post_id);
    } else {
        object.html(non_filled_icon);
    }
}

// post 좋아요 기능 비동기 통신 script
function ILikeThis(dom, target_post){
    var svg = $(dom).find('svg')
    var path = svg.find('path');
    var likes = $(dom).parents('div').prev().children('#likes_count');

    var fill_heart = '<path d="M4 1c2.21 0 4 1.755 4 3.92C8 2.755 9.79 1 12 1s4 1.755 4 3.92c0 3.263-3.234 4.414-7.608 9.608a.513.513 0 0 1-.784 0C3.234 9.334 0 8.183 0 4.92 0 2.755 1.79 1 4 1z"/>';
    var non_fill_heart = '<path fill-rule="evenodd" d="M8 6.236l.894-1.789c.222-.443.607-1.08 1.152-1.595C10.582 2.345 11.224 2 12 2c1.676 0 3 1.326 3 2.92 0 1.211-.554 2.066-1.868 3.37-.337.334-.721.695-1.146 1.093C10.878 10.423 9.5 11.717 8 13.447c-1.5-1.73-2.878-3.024-3.986-4.064-.425-.398-.81-.76-1.146-1.093C1.554 6.986 1 6.131 1 4.92 1 3.326 2.324 2 4 2c.776 0 1.418.345 1.954.852.545.515.93 1.152 1.152 1.595L8 6.236zm.392 8.292a.513.513 0 0 1-.784 0c-1.601-1.902-3.05-3.262-4.243-4.381C1.3 8.208 0 6.989 0 4.92 0 2.755 1.79 1 4 1c1.6 0 2.719 1.05 3.404 2.008.26.365.458.716.596.992a7.55 7.55 0 0 1 .596-.992C9.281 2.049 10.4 1 12 1c2.21 0 4 1.755 4 3.92 0 2.069-1.3 3.288-3.365 5.227-1.193 1.12-2.642 2.48-4.243 4.38z"/>';

    $.ajax({
        url : '/social/like/', // {% url 'social:postLike' %}
        type: 'get',
        data : {'post_id' : target_post},
        dataType: 'json',
        success: function(data){
            if (path.attr('fill-rule') == 'evenodd') {
                svg.html(fill_heart);
                likes.html(data+' likes');
            } else {
                svg.html(non_fill_heart);
                likes.html(data+' likes');
            }
        },
        error : function(err, status){
            alert('로그인 해주세요!!');
            location.href='/account/signIn/'; // {% url 'account:signIn' %}
        }
    });
}

// post 삭제 script
function postDelete(post_id){
    var con = confirm('정말 삭제할까요?');
    if (con == true){
        location.href="/social/delete/?post_id="+post_id; // {% url 'social:postDelete' %}
    }
}


// post 마지막 댓글 가져오는 script
function getLastComment(post_id){
    $.ajax({
        url : '/social/comment/last/', // {% url 'social:getLastComment' %}
        type: 'get',
        data : {'post_id':post_id},
        dataType : 'html',
        success : function(data){
            $('#in_collapse_comments_'+post_id).html(data);
        },
        error : function(request, status, error){
            alert('code:'+request.status+'\nerror:'+error+'\n서버 응답 실패!');
        }
    });
}


// 로그인 페이지로 넘기는 script
function loginRequired(){
    alert('로그인 해주세요!');
    location.href='/account/signIn/';
}


// 무한스크롤 script
 function callMorePostAjax(page) {
    $.ajax( {
    url: '/social/more/', //“{% url ‘post_list_ajax’ %}”,
    type : 'post',
    dataType: 'html',
    data: {
        page: page,
        csrfmiddlewaretoken: csrftoken
    },
    success: addMorePostAjax
    });
}

// 해당 id div tag에 내용을 append
function addMorePostAjax(data) {
    $('#post_list_ajax').append(data);
}


// 댓글 삭제 요청 보내는 script
function commentDelete(comment_id) {
    var trigger = confirm('정말 삭제하시겠어요?')
    if (trigger){
        $.ajax({
            url : '/social/comment/delete/',
            type : 'post',
            data : {
                comment_id : comment_id,
                csrfmiddlewaretoken: csrftoken
            },
            success: function(data){
                alert('삭제 성공!');
                location.reload();
            },
            error : function (request, status, error){
                alert('code:'+request.status+'\nerror:'+error+'\n서버 응답 실패!');
            }
        });
    }
}

function commentCreate(post_id){
    var content = $('#comment_input_text').val()
    $.ajax({
        url : '/social/'+post_id+'/comment/create/',
        type : 'post',
        data : {
            post_id : post_id,
            content : content,
            csrfmiddlewaretoken: csrftoken
        },
        success : function(){
            location.reload();
            alert('댓글 작성 성공!');
        },
        error : function (request, status, error){
            alert('code:'+request.status+'\nerror:'+error+'\n서버 응답 실패!');
        }
    });
}
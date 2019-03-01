$( document ).ready(function() {  // Runs when the document is ready
    // Obatin all post from database
    initial();

    // Add event-handlers
    $("#post-button").click(function (event) {
        addPost();
    });

    //Fetch new posts
    //$.get("/get_post").done(function(data) {
    //    updatePosts()
    //});

    // Refresh the global page every 5 seconds
    window.setInterval(updatePosts, 5000);

    // using jQuery
    // https://docs.djangoproject.com/en/1.10/ref/csrf/

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    var csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
});

//TODO: addPost()
function addPost() {
    var post_field = $('#post-field')
    $.post("/add_post", {'post': post_field.val()}).done(function(data) {
        updatePosts();
        post_field.val("")
    });
}
function addComment(post_id) {
    var comment_list = $('#comment-list' + post_id);
    var comment_field = $('#comment-field'+post_id);
    $.post("/add_comment/" + post_id, {'comment': comment_field.val()}).done(function(data){
        comment_list.append(data.html);
        comment_field.val("")
    });
}

function initial() {
    var post_list = $('#posts-list');
    $.get("/get_post", {'timestamp' : 0.0}).done(function(data) {
        for (var i = 0; i < data.posts.length; i++) {
            var post = data.posts[i];
            var each_post = $(post.html);
            each_post.data('post_id', post.id);
            post_list.prepend(each_post);
            updateComments(post.id);
        }
    });

}

//TODO: Complete update comment
function updateComments(post_id) {
    var comment_list = $('#comment-list' + post_id);
    $.get('/get_comment/' + post_id).done(function(data){
        for (var i = 0; i < data.comments.length; i++) {
            var comment = data.comments[i];
            var each_comment = $(comment.html);
            comment_list.prepend(each_comment);
       }
    })
}

//TODO: getUpdates()
function updatePosts() {
    var posts_list = $('#posts-list');
    var timestamp = $('#timestamp').val();
    // Process posts with posts_id
    $.get("/get_post", {'timestamp' : timestamp}).done(function(data) {
        // Update new post
        for (var i = 0; i < data.posts.length; i++) {
            var post = data.posts[i];
            var new_post = $(post.html);
            new_post.data('post_id', post.id);
            posts_list.prepend(new_post);
        }

        // Update timestamp
        $('#timestamp').val(data.timestamp);
    });
}






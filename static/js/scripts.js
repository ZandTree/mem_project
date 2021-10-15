//setup token

var csrftoken = Cookies.get('csrftoken');
    $.ajaxSetup({
        headers: {"X-CSRFToken": csrftoken}
    });

console.clear();
// language choice

$(".lang").on('submit',function(e){
    e.preventDefault();
    $.ajax({
        url:$(this).attr('action'),
        data:$(this).serialize(),
        method:$(this).attr('method'),
        success:function(resp){
            // location.reload();
            window.location.reload();
        },
        error:function(err){
            console.log(err);
        }
    })
})


// although 2 scripts (ajax login and ajax signup) do the same job, decided to separate them because of error messaging
$(".form-auth").submit(function(e){
     e.preventDefault();
     var url = $(this).attr('action');
     var data = $(this).serialize();
     $.ajax({
        url,
        data,
        method:$(this).attr('method'),
        success:function(response){
            location.reload();
        },
        error:function(err){
            var errLogin = err.responseJSON.form.errors;
            var alertSignUp = $(".alert-signup");
            alertSignUp.html(errLogin);
            var mail = $(".er-email");
            var psw1 = $(".er-psw1");
            var psw2 = $(".er-psw2");

            if(err.responseJSON.form.fields.email.errors){
                mail.html(err.responseJSON.form.fields.email.errors);
            }
            if(err.responseJSON.form.fields.password1.errors){
                psw1.html(err.responseJSON.form.fields.password1.errors);

            }
            if(err.responseJSON.form.fields.password2.errors){
                psw2.html(err.responseJSON.form.fields.password2.errors);

            }
        }
    }
);
})
// login ajax
// although 2 scripts (ajax login and ajax signup) do the same job, decided to separate them because of error messaging
$(".form-auth-login").submit(function(e){
     e.preventDefault();
     var url = $(this).attr('action');
     var data = $(this).serialize();
     $.ajax({
        url,
        data,
        method:$(this).attr('method'),
        success:function(response){
            location.reload();
        },
        error:function(err){
            var alertLogin = $(".alert-login");
            var errLogin = err.responseJSON.form.errors;
            //console.log("all errors:",errLogin);
            alertLogin.html(errLogin);
            var lgin = $(".login-error");
            var psw = $("password-error");
            if(err.responseJSON.form.fields.login.errors){
                lgin.html(err.responseJSON.form.fields.login.errors)
            }
            if(err.responseJSON.form.fields.password.errors){
                psw.html(err.responseJSON.form.fields.password.errors)
            }
        }
    }
);
})

// console.clear();
const navSlide =()=>{
    const burger = document.querySelector('.burger');
    const nav = document.querySelector('.nav-links');
    // lets take all li's in ul
    const navLinks = document.querySelectorAll('.nav-links li');

    //toggle nav
    burger.addEventListener('click',()=>{
        nav.classList.toggle('nav-active');
        //animate links
        navLinks.forEach((link,index)=>{
            if(link.style.animation){
                link.style.animation=""
            }
            else {
                link.style.animation=`navLinkFade 0.5s ease forwards ${index/7 + 0.3}s`;
            }
        });
        //burger animation
        burger.classList.toggle('toggle');
    }) //end addEventListener

} // end function navLinks
navSlide();

// let op: below |==> modal with error dus codes below it dont't work
$(".footer-nav-menu-item").on('click',function(){
    console.log("click in the footer")
    var label = $(this).attr('data-label');
    // let op: need to remove class .active from all prev opened panels
    $(".panel").removeClass("active");
    $(`#${label}`).addClass("active"); // give transform="translateY(0%)
})
$(".panel-close").on('click',function(){
    $(".panel").removeClass("active"); // give transform="translateY(1000%)
})

// modal functionality

// signup
// plus effect: .call-button disappear
let  wakeModalSignUp = $('.modal-btn-signup');
let modalShow = $(".modal-bg-signup");
let callBtn = $(".call-button");

wakeModalSignUp.on('click',function(){
    console.log("found your modalBtn");
    modalShow.addClass('modal-bg-active');
    // click event|=>.call-button disappear
    callBtn.hide();
})


//close modal
let modalClose = $('.modal-close')
modalClose.on('click',function(){
    modalShow.removeClass('modal-bg-active');
    callBtn.show();
})
//login
let modalButLogIn = $(".modal-btn-login");
let modalLogIn = $(".modal-bg-login");
modalButLogIn.on('click',function(){
    modalLogIn.addClass('modal-bg-active');
    callBtn.hide();
})


//close modal-2
let modalClose2 = $(".modal-close2");
modalClose2.on('click',function(){
    modalLogIn.removeClass('modal-bg-active');
    callBtn.show()
})

let callLogin = $("#loginCall");
callLogin.on('click',function(){
    modalShow.removeClass('modal-bg-active');
    modalLogIn.addClass('modal-bg-active')
})

let callSignUp = $('#call-signup');
callSignUp.on('click',function(){
    modalLogIn.removeClass('modal-bg-active');
    modalShow.addClass('modal-bg-active');
})

// widget datepicker Fengyuan Chen
// $(function () {
//      $("#datepicker").datepicker();
//    });


// footer animation
// click event for footer items with change in css property transform
// my solution
// footerItem.addEventListener('click',()=>{
//     bookshelf.style.transform="translateY(0%)";
// })
// crossX.addEventListener('click',()=>{
//     bookshelf.style.transform="translateY(100%)";
// })

// brian solution

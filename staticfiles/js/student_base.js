let isToggleVisible = false;

function toggleNavigation(){
    let navigation = $('.navigation')[0];
    let t = $('toggle');

    if(isToggleVisible == false){
        navigation.className = "navigation navigation-toggled";
        isToggleVisible = true;
    }else{
        navigation.className = "navigation";
        isToggleVisible = false;
    }
}
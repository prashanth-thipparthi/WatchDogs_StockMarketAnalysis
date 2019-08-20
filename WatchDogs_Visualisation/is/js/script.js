//function fadeOutAndCallback(image, callback){
//	var opacity = 1;
//	var timer = setInterval(function(){
//		if(opacity < 0.1){
//			clearInterval(timer);
//			callback(); //this executes the callback function!
//		}
//		image.style.opacity = opacity;
//		opacity -=  0.1;
//	}, 50);
//}
//
//fadeOutAndCallback(image,
//	function(){
//		image.src = newImage.src;
//		fadeIn(image);
//	}
//);

function changeImage(imageId, imageName){
	document.getElementById(imageId).src=imageName;
}

var bigSwitch=document.getElementById("switcharoo");
bigSwitch.addEventListener("mouseover", function(){
	changeImage("switcharoo", "img/watchdogslogoEnter2.png");
});

bigSwitch.addEventListener("mouseout", function(){
	changeImage("switcharoo", "img/watchdogslogoEnter.png");
});
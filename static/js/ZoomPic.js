
function ZoomPic ()
{
	this.initialize.apply(this, arguments)
}
ZoomPic.prototype =
{
	initialize : function (id)
	{
		var _this = this;
		this.wrap = typeof id === "string" ? document.getElementById(id) : id;
		this.oUl = this.wrap.getElementsByTagName("ul")[0];
		this.aLi = this.wrap.getElementsByTagName("li");
		this.prev = this.wrap.getElementsByTagName("span")[0];
		this.next = this.wrap.getElementsByTagName("span")[1];
		this.timer = 1000;
		this.aSort = [];
		this.iCenter = 2;
		this._doPrev = function () {return _this.doPrev.apply(_this)};
		this._doNext = function () {return _this.doNext.apply(_this)};
		this.options = [
			{width:746, height:210, top:24, left:0, zIndex:1},
			{width:746, height:234, top:8, left:80, zIndex:2},
			{width:746, height:255, top:0, left:160, zIndex:3},
			{width:746, height:234, top:8, left:240, zIndex:2},
			{width:746, height:210, top:24, left:300, zIndex:1},
		];
		for (var i = 0; i < this.aLi.length; i++) this.aSort[i] = this.aLi[i];
		this.aSort.unshift(this.aSort.pop());
		//this.aSort.push(this.aSort.shift())
		this.setUp();
		this.addEvent(this.prev, "click", this._doPrev);
		this.addEvent(this.next, "click", this._doNext);
		this.doImgClick();
		this.timer = setInterval(function ()
		{
			//_this.doPrev()//自动向右旋转
			_this.doNext()//自动向左旋转
		}, 5000);
		this.wrap.onmouseover = function ()
		{
			clearInterval(_this.timer)
		};

	},
	doPrev : function ()
	{
		this.aSort.unshift(this.aSort.pop());
		this.setUp()
	},
	doNext : function ()
	{
		this.aSort.push(this.aSort.shift());
		this.setUp()
	},
	doImgClick : function ()
	{
		var _this = this;
		for (var i = 0; i < this.aSort.length; i++)
		{
			this.aSort[i].onclick= function ()
			//this.aSort[i].onmouseover= function ()
			{
				if (this.index > _this.iCenter)
				{
					for (var i = 0; i < this.index - _this.iCenter; i++) _this.aSort.push(_this.aSort.shift());
					_this.setUp()

				}
				else if(this.index < _this.iCenter)
				{
					for (var i = 0; i < _this.iCenter - this.index; i++) _this.aSort.unshift(_this.aSort.pop());
					_this.setUp()
				}
			}
		}
	},
	setUp : function ()
	{
		var _this = this;
		var i = 0;
		for (i = 0; i < this.aSort.length; i++) this.oUl.appendChild(this.aSort[i]);
		for (i = 0; i < this.aSort.length; i++)
		{
			this.aSort[i].index = i;
			if (i < 5)
			{
				this.css(this.aSort[i], "display", "block");
				// if(i!=2){
				// 		this.aSort[i].getElementsByTagName("p")[0].style.display="none"
				// 	}
				this.doMove(this.aSort[i], this.options[i], function ()
				{

					_this.doMove(_this.aSort[_this.iCenter].getElementsByTagName("img")[0], {opacity:100}, function ()
					{

						_this.aSort[_this.iCenter].getElementsByTagName("p")[0].style.display="block";
						/*_this.doMove(_this.aSort[_this.iCenter].getElementsByTagName("img")[0], {opacity:100}, function ()
						{
							_this.aSort[_this.iCenter].onmouseover = function ()
							{
								_this.doMove(this.getElementsByTagName("div")[0], {bottom:0})
							};
							_this.aSort[_this.iCenter].onmouseout = function ()
							{
								_this.doMove(this.getElementsByTagName("div")[0], {bottom:-100})
							}
						})*/
					})
				});
			}
			else
			{
				this.css(this.aSort[i], "display", "none");
				this.css(this.aSort[i], "width", 0);
				this.css(this.aSort[i], "height", 0);
				this.css(this.aSort[i], "top", 37);
				this.css(this.aSort[i], "left", this.oUl.offsetWidth / 2)
			}
			//console.log(this.iCenter)
			if (i < this.iCenter || i > this.iCenter)
			{
				this.aSort[i].getElementsByTagName("p")[0].style.display="none";

				//this.css(this.aSort[i].getElementsByTagName("img")[0], "opacity", 100)
				this.aSort[i].onmouseover = function ()
				{
					_this.doMove(this.getElementsByTagName("img")[0], {opacity:100})
				};
				this.aSort[i].onmouseout = function ()
				{
					_this.doMove(this.getElementsByTagName("img")[0], {opacity:50})
				};
				this.aSort[i].onmouseout();
			}
			else
			{
				this.aSort[i].onmouseover = this.aSort[i].onmouseout = null
			}
			if (i == this.iCenter){

				//this.aSort[i].style.borderBottom="3px solid #d1c0a5"
				//console.log(this.aSort[i].style.borderBottom)
			}else if(i == 1 || i == 3){
				//this.aSort[i].style.borderBottom="3px solid #f8b551"
			}else if(i == 0 || i == 4){
				//this.aSort[i].style.borderBottom="3px solid #84ccc9"
			}
		}
	},
	addEvent : function (oElement, sEventType, fnHandler)
	{
		return oElement.addEventListener ? oElement.addEventListener(sEventType, fnHandler, false) : oElement.attachEvent("on" + sEventType, fnHandler)
	},
	css : function (oElement, attr, value)
	{


		if (arguments.length == 2)
		{
			return oElement.currentStyle ? oElement.currentStyle[attr] : getComputedStyle(oElement, null)[attr]
		}
		else if (arguments.length == 3)
		{
			switch (attr)
			{
				case "width":
				case "height":
				case "top":
				case "left":
				case "bottom":
					oElement.style[attr] = value + "px";
					break;
				case "opacity" :
				 	oElement.style.filter = "alpha(opacity=" + value + ")";
				 	oElement.style.opacity = value / 100;
					break;
				default :
					oElement.style[attr] = value;
					break
			}
			//console.log(oElement.style[attr])
		}
	},
	doMove : function (oElement, oAttr, fnCallBack)
	{
		var _this = this;
		clearInterval(oElement.timer);
		//console.log(oElement)
		oElement.timer = setInterval(function ()
		{
			var bStop = true;
			for (var property in oAttr)
			{
				var iCur = parseFloat(_this.css(oElement, property));
				property == "opacity" && (iCur = parseInt(iCur.toFixed(2) * 100));
				var iSpeed = (oAttr[property] - iCur) / 5;
				iSpeed = iSpeed > 0 ? Math.ceil(iSpeed) : Math.floor(iSpeed);

				if (iCur != oAttr[property])
				{
					bStop = false;
					_this.css(oElement, property, iCur + iSpeed)
				}
			}
			if (bStop)
			{
				clearInterval(oElement.timer);
				fnCallBack && fnCallBack.apply(_this, arguments)
			}
		}, 30)

	}
};
window.onload = function ()
{
	new ZoomPic("listenBox");
};
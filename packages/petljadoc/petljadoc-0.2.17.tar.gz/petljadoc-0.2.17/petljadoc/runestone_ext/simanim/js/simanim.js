pythonInitialized = false;

SIM_STATUS_STOPPED = 1
SIM_STATUS_PLAYING = 2
SIM_STATUS_PAUSED = 3
SIM_STATUS_FINISHED = 4

simanimList = {}

function SimAnim (opts) {
    if (opts) {
        this.init(opts);
    }
}

SimAnim.prototype.init = async function(opts){
	this.opts = opts
	this.id = opts.id
	this.simStatus = SIM_STATUS_STOPPED
	this.code = popAttribute(opts,'data-code',"") 
	this.imgPath = popAttribute(opts,'data-img-path',"")
	this.scale = parseFloat(popAttribute(opts,'data-scale',"1"))
	this.pythonError = false
	this.pythonErrorMsg = ""
	this.varsInputElementId = {}
	this.eventQue = []
	this.simImages = {}
	this.drawFunctions = {'circle' : this.drawCircle,
						  'box' : this.drawBox,
						  'line' : this.drawLine, 
						  'triangle' : this.drawTriangle,
						  'polyLine' : this.drawPolyLine,
						  'image' : this.drawImage,
						  'text' : this.drawText,
						  'rotate' : this.rotate,
						  'restore' : this.restore
						}
	await this.execPython()
	if(this.pythonError){
	   console.log('Animation id: '+ this.id + '\nPython error:\n')
	   console.log(this.pythonErrorMsg)
	}
	else{
		this.generateHTMLForSim() 
		this.setupCanvas()
	}
}

SimAnim.prototype.execDrawing = async function(){
	for(var i =0; i < this.eventQue.length; i++){
		await this.eventQue[i]()
	}
	this.eventQue = []
}

SimAnim.prototype.setupCanvas = function() {
	// settings
	this.ctx.canvas.width = this.animation_instance.anim_context.settings.window_with_px * this.scale;
	this.ctx.canvas.height = this.animation_instance.anim_context.settings.window_height_px * this.scale;

	this.scale =  this.animation_instance.anim_context.settings.px_per_unit * this.scale
	this.animation_instance_x_min = this.animation_instance.anim_context.settings.view_box[0][0]
	this.animation_instance_y_min  =  this.animation_instance.anim_context.settings.view_box[0][1]
	this.animation_instance_height = this.animation_instance.anim_context.settings.view_box[2]
	this.update_period = this.animation_instance.anim_context.settings.update_period
	this.background_color =  this.animation_instance.anim_context.settings.background_color

	//drawing
	this.ctx.fillStyle = this.background_color
	this.ctx.fillRect(0, 0, this.ctx.canvas.width, this.ctx.canvas.height);
	this.animation_instance.queueFrame(); // setting up frist frame / thumbnail
	this.execDrawing()
}

SimAnim.prototype.setPythonErrorMsg = function(errMsg){
		this.pythonError = true
		this.pythonErrorMsg = errMsg
}

SimAnim.prototype.execPython = function(){
	pyodide.globals.the_script = this.code
	return pyodide.runPythonAsync(`
			try:
				exec(the_script,{'animation_instance_key' : '${this.id}'})
			except Exception:
				exc_type, exc_value, exc_tb = sys.exc_info()
				error_msg = ''.join(traceback.format_exception(exc_type, exc_value, exc_tb.tb_next))
				js.throwError(error_msg)
			else:
				import simanim.pyodide.gui	
			`)
		.then(() => {				
			this.animation_instance = pyodide.globals.simanim.pyodide.gui.animation_instance[this.id]
		})
		.catch((msg) => {this.setPythonErrorMsg(msg);})
}

SimAnim.prototype.generateHTMLForSim = function() {
	var simDiv = document.createElement('div');
	simDiv.setAttribute('class', 'modal-sim');

	var simDivContent = document.createElement('div');
	simDivContent.setAttribute('class', 'modal-content-sim');

	var simDivControls = document.createElement('div');
	simDivControls.setAttribute('class', 'sim-controls');

	var controlBtnDiv = document.createElement('div');
	controlBtnDiv.setAttribute('class', 'control-button-div');

	this.playBtn = document.createElement('button');
	this.playBtn.setAttribute('class', 'control-btn');
	this.playBtn.addEventListener('click', this.startSim.bind(this));
	this.playBtn.innerHTML = '<i class="fas fa-play"></i> PLAY';

	this.stopBtn = document.createElement('button');
	this.stopBtn.setAttribute('class', 'control-btn');
	this.stopBtn.setAttribute('disabled', 'disabled');
	this.stopBtn.addEventListener('click', this.stopSim.bind(this));
	this.stopBtn.innerHTML = '<i class="fas fa-stop"></i> STOP';

	this.pauseBtn = document.createElement('button');
	this.pauseBtn.setAttribute('class', 'control-btn d-none');
	this.pauseBtn.addEventListener('click', this.pauseSim.bind(this));
	this.pauseBtn.innerHTML = '<i class="fas fa-pause"></i> PAUSE';

	controlBtnDiv.appendChild(this.playBtn);
	controlBtnDiv.appendChild(this.pauseBtn);
	controlBtnDiv.appendChild(this.stopBtn);
	
	simDivControls.appendChild(controlBtnDiv);

	var variablesDiv = document.createElement('div');
	variablesDiv.setAttribute('class', 'sim-modal-variables');
	variablesDiv.setAttribute('id', 'variablesDiv');

	var variables = this.animation_instance.getVars();
	for (var i = 0; i < variables.length; i++) {
		if (variables[i].meta["type"] == 'InputFloat') {
			var variableLabel = document.createElement('label');
			variableLabel.setAttribute('class', 'variable-label');
			variableLabel.innerHTML = `${variables[i].name} = `;

			var max = variables[i]['meta']['limit_to']
			var step = Math.pow(10,Math.floor(Math.log10(max)-1))

			var variableInput = document.createElement('input');
			variableInput.setAttribute('type', 'number');
			variableInput.setAttribute('class', 'variable-input');	
			variableInput.setAttribute('id', this.id + '-' +i)		
			variableInput.setAttribute('value', '' + variables[i]['meta']['default']);
			variableInput.setAttribute('min',variables[i]['meta']['limit_from'])
			variableInput.setAttribute('max',variables[i]['meta']['limit_to'])		
			variableInput.setAttribute('step', step);
			variableInput.addEventListener('input',this.setGetters.bind(this))

			this.varsInputElementId[variables[i].name] = this.id + '-' +i	

			variablesDiv.appendChild(variableLabel);
			variablesDiv.appendChild(variableInput);
		}
		else {
			var variableLabel = document.createElement('label');
			variableLabel.setAttribute('class', 'variable-label');
			variableLabel.innerHTML = `${variables[i].name} = `;

			var selectInput = document.createElement('select');
			selectInput.setAttribute('class', 'variable-input')
			selectInput.setAttribute('id', this.id + '-' +i)
			selectInput.addEventListener('input',this.setGetters.bind(this))

			for (var j = 0; j < variables[i].meta.lov.length; j++) {
				var selectOption = document.createElement('option');
				selectOption.innerHTML = variables[i].meta.lov[j];
				if(variables[i].meta.lov[j] == variables[i].meta.default){
					selectOption.setAttribute('selected','selected')	
				}
				selectInput.appendChild(selectOption);
			}
			this.varsInputElementId[variables[i].name] = this.id + '-' +i

			variablesDiv.appendChild(variableLabel);
			variablesDiv.appendChild(selectInput);
		}
	}

	simDivControls.appendChild(variablesDiv);

	var simBodyCanvasDiv = document.createElement('div');
	simBodyCanvasDiv.setAttribute('class', 'sim-modal-canvas');

	this.canvas = document.createElement('canvas');
	this.canvas.setAttribute('id', 'simCanvas-' + this.id);
	this.canvas.setAttribute('class', ' sim-canvas')
	this.ctx = this.canvas.getContext('2d');

	simBodyCanvasDiv.appendChild(this.canvas);
	simDivContent.appendChild(simDivControls);
	simDivContent.appendChild(simBodyCanvasDiv);

	simDiv.appendChild(simDivContent);
	this.opts.appendChild(simDiv);

}

SimAnim.prototype.startSim = function() {
	this.playBtn.classList.add('d-none');
	this.pauseBtn.classList.remove('d-none');
	this.stopBtn.removeAttribute('disabled');

	for (var varName in this.varsInputElementId) {
		document.getElementById(this.varsInputElementId[varName]).setAttribute('disabled','true')
	}
	this.simStatus = SIM_STATUS_PLAYING;
	this.startDrawing.call(this)
}

SimAnim.prototype.setGetters =  function(){
	variableValues = {}
	for (var varName in this.varsInputElementId) {
		variableValues[varName] = this.varsInputElementId[varName] 
	}
	this.animation_instance.setVarGetters(variableValues) // resets the animation to the begining
	this.clearAndDraw()
}

SimAnim.prototype.clearAndDraw =  function(){
	this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
	this.ctx.fillRect(0, 0, this.ctx.canvas.width, this.ctx.canvas.height);
	this.animation_instance.queueFrame();
	this.execDrawing()
}

SimAnim.prototype.startDrawing =  function(){
	var startDrawing =  window.performance.now();
	if (!this.animation_instance.getEndAnimation() && this.simStatus == SIM_STATUS_PLAYING) {
	     this.clearAndDraw()
		var endDrawing = window.performance.now();
		//console.log('Next frame drawn in '+ (this.update_period*1000 - (endDrawing - startDrawing)/1000) +' s')
		//console.log('Frame drawn in '+(endDrawing - startDrawing)/1000+' s')
		this.timeoutFunc = setTimeout(() => {this.startDrawing.call(this)}, this.update_period*1000 - (endDrawing - startDrawing)/1000);
	}
	else if (this.animation_instance.getEndAnimation()){
		this.clearAndDraw()

		this.simStatus = SIM_STATUS_FINISHED
		this.playBtn.classList.remove('d-none');
		this.playBtn.setAttribute('disabled', 'disabled');
		this.pauseBtn.classList.add('d-none');
	
		clearTimeout(this.timeoutFunc)
	}
}

SimAnim.prototype.cleanUp = function(){
	this.simStatus = SIM_STATUS_STOPPED
	this.ctx.clearRect(0, 0, this.ctx.canvas.width, this.ctx.canvas.height);
	this.ctx.fillRect(0, 0, this.ctx.canvas.width, this.ctx.canvas.height)
	this.animation_instance.resetAnimation();
	this.execDrawing()

	this.playBtn.classList.remove('d-none');
	this.playBtn.removeAttribute('disabled');
	this.pauseBtn.classList.add('d-none');
	this.stopBtn.setAttribute('disabled', 'disabled');

	for (var varName in this.varsInputElementId) {
		document.getElementById(this.varsInputElementId[varName]).removeAttribute('disabled')
	}

	clearTimeout(this.timeoutFunc);
}

SimAnim.prototype.stopSim = function() {
	this.cleanUp()
}

SimAnim.prototype.pauseSim = function() {
	this.playBtn.classList.remove('d-none');
	this.pauseBtn.classList.add('d-none');
	this.simStatus = SIM_STATUS_PAUSED
}

SimAnim.prototype.queueDrawEvent = function(type, obj){
	this.eventQue.push(this.drawFunctions[type].bind(this, obj))
}

SimAnim.prototype.scalarToPixel = function(scalar){
	return scalar * this.scale
}

SimAnim.prototype.pointToPixel = function(point){
	var scalarPointX = this.scalarToPixel(point[0] - this.animation_instance_x_min)
	var scalarPointY = this.scalarToPixel(this.animation_instance_y_min + this.animation_instance_height - point[1])
	return [scalarPointX, scalarPointY]
}
SimAnim.prototype.rectToPixel = function(rect){
	var xy_min = this.pointToPixel([rect.xy_min[0],rect.xy_min[1] + rect.height])
	var width = this.scalarToPixel(rect.width)
	var height = this.scalarToPixel(rect.height)
	return [xy_min, width, height]
}

SimAnim.prototype.drawCircle = function(circle){
	this.ctx.save()
	this.ctx.fillStyle = circle.fill_color;
	this.ctx.strokeStyle = circle.pen_color
	this.ctx.lineWidth = this.scalarToPixel(circle.line_width);
	if (this.ctx.line_dashed) {
		this.ctx.setLineDash([5, 5])
	}
	var center = this.pointToPixel(circle.center)
	var radius = this.scalarToPixel(circle.radius)
	this.ctx.beginPath();
	this.ctx.arc(center[0], center[1], radius, 0, 2 * Math.PI, false);
	this.ctx.closePath();
	this.ctx.fill();
	this.ctx.stroke();
	this.ctx.restore();
}

SimAnim.prototype.drawBox = function(rect) {
	this.ctx.save()
	this.ctx.lineWidth  = rect.line_width ?  this.scalarToPixel(rect.line_width)  : 1
	this.ctx.fillStyle = rect.fill_color;
	this.ctx.strokeStyle = rect.pen_color ? rect.pen_color : rect.fill_color 
	if (rect.line_dashed) {
		this.ctx.setLineDash([5, 5])
	}
	var scaledRect = this.rectToPixel(rect)
	this.ctx.beginPath();
	this.ctx.rect(scaledRect[0][0], scaledRect[0][1], scaledRect[1], scaledRect[2]);
	this.ctx.closePath();
	this.ctx.fill();
	this.ctx.stroke();

	this.ctx.restore()
}

SimAnim.prototype.drawLine = function(line) {
	this.ctx.save()
	this.ctx.strokeStyle = line.pen_color
	this.ctx.lineWidth = this.scalarToPixel(line.line_width);
	if (line.line_dashed) {
		this.ctx.setLineDash([5, 5])
	}
	this.ctx.beginPath();
	var point1 = this.pointToPixel(line.point1)
	var point2 = this.pointToPixel(line.point2)
	this.ctx.moveTo(point1[0], point1[1]);
	this.ctx.lineTo(point2[0], point2[1]);
	this.ctx.stroke();
	this.ctx.restore()
}
SimAnim.prototype.drawPolyLine = function(polyLine) {
	this.ctx.save()
	var numberOfPoints = polyLine.points.length
	if (numberOfPoints < 1) {
		return;
	}
	let points = polyLine.points
	this.ctx.fillStyle = polyLine.fill_color;
	this.ctx.strokeStyle = polyLine.pen_color
	this.ctx.lineWidth = this.scalarToPixel(polyLine.line_width);
	if (polyLine.line_dashed) {
		this.ctx.setLineDash([5, 5])
	}
	this.ctx.beginPath();
	var scalarPointX 
	var scalarPointY 
	[scalarPointX, scalarPointY] = this.pointToPixel(points[0])
	this.ctx.moveTo(scalarPointX,scalarPointY)
	for (i = 1; i < numberOfPoints; i++) {
		[scalarPointX, scalarPointY] = this.pointToPixel(points[i])
		this.ctx.lineTo(scalarPointX,scalarPointY)
	};
	this.ctx.stroke();
	this.ctx.restore()
}
//triangle[6] canvas settings
//trinagle[0] point 1  X
//trinagle[1] point 1  Y
//trinagle[2] point 2  X
//trinagle[3] point 2  Y
//trinagle[4] point 3  X
//trinagle[5] point 3  Y
SimAnim.prototype.drawTriangle = function(triangle) {
	this.ctx.save()
	this.ctx.strokeStyle = triangle[6].pen_color;
	this.ctx.lineWidth  = this.scalarToPixel(triangle[6].line_width);
	this.ctx.fillStyle = triangle[6].pen_color;
	if (triangle[6].line_dashed) {
		this.ctx.setLineDash([5, 5])
	}
	var point1 = this.pointToPixel([triangle[0],triangle[1]])
	var point2 = this.pointToPixel([triangle[2],triangle[3]])
	var point3 = this.pointToPixel([triangle[4],triangle[5]])
	this.ctx.beginPath();
	var path=new Path2D()
	path.moveTo(point1[0], point1[1]);
	path.lineTo(point2[0], point2[1]);
	path.lineTo(point3[0], point3[1]);
	this.ctx.fill(path);
	this.ctx.stroke();
	this.ctx.restore()
}

SimAnim.prototype.drawImage = function(image) {
	this.ctx.save()
	return new Promise(function (resolve){
		if (image.file in this.simImages)
			resolve(image)
		else {
			this.simImages[image.file] = new Image();
			this.simImages[image.file].onload = () => {
				resolve(image)
			}
			this.simImages[image.file].src = pathJoin([this.imgPath, image.file]);
		}
		
	}.bind(this)).then((image) => {
		var xy_min = this.pointToPixel([image.xy_min[0],image.xy_min[1] + image.height])
		var width = this.scalarToPixel(image.width)
		var height = this.scalarToPixel(image.height)
		this.ctx.drawImage(this.simImages[image.file], xy_min[0], xy_min[1], width, height);
		this.ctx.restore()
	});

}

//text.position [X,Y] 

SimAnim.prototype.drawText = function(text) {
	this.ctx.save()
	this.ctx.fillStyle = 'black'
	var font_size = this.scalarToPixel(text.font_size)
	this.ctx.font = `bold ${font_size}px Courier New`;
	var position = this.pointToPixel(text.position)
	this.ctx.fillText(text.content, position[0], position[1]);
	this.ctx.restore()
}

SimAnim.prototype.restore = function() {
	this.ctx.setTransform(1, 0, 0, 1, 0, 0);
}
//point[0] point around which we rotate
//point[1] angle
SimAnim.prototype.rotate = function(point) {
	var scaledPoint = this.pointToPixel(point[0])
	this.ctx.translate( scaledPoint[0], scaledPoint[1]);
	this.ctx.rotate(point[1]);
	this.ctx.translate(- scaledPoint[0], - scaledPoint[1]);
}

window.addEventListener('load',function() {
	// init pyodide
	languagePluginLoader.then(() =>
		pyodide.runPythonAsync(`
	import sys
	import traceback
	import io
	import js
	import micropip
	micropip.install('utils')
	micropip.install('${document.location.origin}/_static/simanim-0.3.1-py3-none-any.whl').then(js.pythonInicijalizovan())
	`)
	).then(() => {
		animations = document.getElementsByClassName('simanim')
		for (var i = 0; i < animations.length; i++) {
			simanimList[animations[i].id] = new SimAnim(animations[i])			
		}
	});

});

function pythonInicijalizovan() {
	pythonInitialized = true;
}

function queDrawEvent(event){
	simanimList[event.animation_key].queueDrawEvent(event.type,event.object)
}

function pathJoin(parts, sep){
	var separator = sep || '/';
	var replace   = new RegExp(separator+'{1,}', 'g');
	return parts.join(separator).replace(replace, separator);
 }
 
 function popAttribute(element, atribute, fallback){
	var atr = fallback;
	if (element.hasAttribute(atribute)){
		atr = element.getAttribute(atribute)
		element.removeAttribute(atribute)
	}
	return atr;
 }

 function throwError(msg){
	throw msg
}
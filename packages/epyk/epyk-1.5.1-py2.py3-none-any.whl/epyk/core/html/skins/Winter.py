#!/usr/bin/python
# -*- coding: utf-8 -*-

from epyk.core.html.graph import GraphCanvas

"""
canvas{
    position:absolute;top:0;left:0
    background-image: linear-gradient(bottom, rgb(105,173,212) 0%, rgb(23,82,145) 84%);
    background-image: -o-linear-gradient(bottom, rgb(105,173,212) 0%, rgb(23,82,145) 84%);
    background-image: -moz-linear-gradient(bottom, rgb(105,173,212) 0%, rgb(23,82,145) 84%);
    background-image: -webkit-linear-gradient(bottom, rgb(105,173,212) 0%, rgb(23,82,145) 84%);
    background-image: -ms-linear-gradient(bottom, rgb(105,173,212) 0%, rgb(23,82,145) 84%);
    
    background-image: -webkit-gradient(
        linear,
        left bottom,
        left top,
        color-stop(0, rgb(105,173,212)),
        color-stop(0.84, rgb(23,82,145))
    );
}
"""


class WinterSnow(GraphCanvas.Canvas):
  name = 'Skin Winter Snow'
  #
  # @property
  # def style(self):
  #   """
  #   Description:
  #   ------------
  #   Property to the CSS Style of the component
  #
  #   """
  #   if self._styleObj is None:
  #     self._styleObj = GrpClsJqueryUI.ClassSlider(self)
  #   return self._styleObj

  @property
  def cursors(self):
    pass

  _js__builder__ = '''
  var requestAnimationFrame = window.requestAnimationFrame || window.mozRequestAnimationFrame || window.webkitRequestAnimationFrame || window.msRequestAnimationFrame ||
  function(callback){window.setTimeout(callback, 1000 / 60)}; window.requestAnimationFrame = requestAnimationFrame;
  window.flakes = []; window.flakeCount = 400; var mX = -100; var mY = -100;
  htmlObj.width = window.innerWidth; htmlObj.height = window.innerHeight;
  htmlObj.addEventListener("mousemove", function(e) {mX = e.clientX, mY = e.clientY});
  window.addEventListener("resize", function(){htmlObj.width = window.innerWidth; htmlObj.height = window.innerHeight})
  for (var i = 0; i < window.flakeCount; i++) {
    var x = Math.floor(Math.random() * htmlObj.width); var y = Math.floor(Math.random() * htmlObj.height);
    var size = (Math.random() * 3) + 2; var speed = (Math.random() * 1) + 0.5;
    var opacity = (Math.random() * 0.5) + 0.3;
    window.flakes.push({speed: speed, velY: speed, velX: 0, x: x, y: y, size: size, stepSize: (Math.random()) / 30,
        step: 0, opacity: opacity})};
  startSnow()
'''

  def __str__(self):
    self._report._props.setdefault('js', {}).setdefault("builders", []).append(self.refresh())
    constructors = self._report._props.setdefault("js", {}).setdefault("constructors", {})
    constructors['resetSnow'] = '''
function resetSnow(flake){
  var canvas = document.getElementById("%s");
  flake.x = Math.floor(Math.random() * canvas.width); flake.y = 0; flake.size = (Math.random() * 3) + 2;
  flake.speed = (Math.random() * 1) + 0.5; flake.velY = flake.speed; flake.velX = 0;
  flake.opacity = (Math.random() * 0.5) + 0.3}''' % self.htmlCode

    constructors['startSnow'] = '''
function startSnow() { var mX = -100; var mY = -100;
  var canvas = document.getElementById("%s");  var ctx = canvas.getContext("2d"); 
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  for (var i = 0; i < window.flakeCount; i++) {
    var flake = window.flakes[i]; var x = mX; var y = mY; var minDist = 150; var x2 = flake.x; var y2 = flake.y;
    var dist = Math.sqrt((x2 - x) * (x2 - x) + (y2 - y) * (y2 - y)); var dx = x2 - x; var dy = y2 - y;
    if (dist < minDist) {
      var force = minDist / (dist * dist); var xcomp = (x - x2) / dist; var ycomp = (y - y2) / dist; 
      var deltaV = force / 2; flake.velX -= deltaV * xcomp; flake.velY -= deltaV * ycomp} 
    else {
      flake.velX *= .98; if (flake.velY <= flake.speed){flake.velY = flake.speed};
      flake.velX += Math.cos(flake.step += .05) * flake.stepSize}
    ctx.fillStyle = "rgba(255,255,255," + flake.opacity + ")";
    flake.y += flake.velY; flake.x += flake.velX;
    if (flake.y >= canvas.height || flake.y <= 0) {resetSnow(flake)}
    if (flake.x >= canvas.width || flake.x <= 0) {resetSnow(flake)}
    ctx.beginPath(); ctx.arc(flake.x, flake.y, flake.size, 0, Math.PI * 2); ctx.fill()}
  requestAnimationFrame(startSnow)}''' % self.htmlCode
    return "<canvas %s>Your browser does not support the HTML5 canvas tag.</canvas>" % (self.get_attrs(pyClassNames=self.style.get_classes()))


// ==UserScript==
// @name          Remove Yahoo! Group Links on Reply
// @namespace     http://pythonologia.org
// @description   This script removes the Yahoo! Groups links at the end of message when replying a message on Gmail.
// @include       https://mail.google.tld/mail/*
// @include       http://mail.google.tld/mail/*
// @include       https://mail.google.tld/a/*
// @include       http://mail.google.tld/a/*
// ==/UserScript==

document.addEventListener('focus', function(event) {

	// Bail if the focused element is not a reply form
	if (!event.target.id || !event.target.id.match(/^ta_\d+$/)) return;
	var textarea = event.target, body = textarea.value;
	
	// Bail if contents don't match the default top-posting (e.g. if we modified it already)
	if (!body.match(/>\sLinks do Yahoo!/)) return;
 
	body = body.replace(/>\sLinks do Yahoo!.*\n> \n(.*\n){10}/, ''); // clean Y!Groups headers
	body = body.replace(/> ,---.*.\n(.*\n){5}/, ''); // Clean python-brasil box

	textarea.value = body;
}, true);

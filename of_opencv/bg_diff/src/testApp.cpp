#include "testApp.h"

//--------------------------------------------------------------
void testApp::setup(){
    
    ofSetVerticalSync(true);
    ofSetFrameRate(60);
    
    _width = 240;
    _height = 135;
    _learnRate = .1;
    _threshold = 50;
    
    _source = cvLoadImageM("data/logo.png");
    if( _source == NULL ) {
        ofLogError() << "Could not load image" << endl;
    } else {
        ofxCv::toOf( _source, _img );
        ofLog(OF_LOG_NOTICE, "Successfully loaded image");
    }
    
}

//--------------------------------------------------------------
void testApp::update() {

}

//--------------------------------------------------------------
void testApp::draw() {
	
    char fr[10];
    snprintf( fr, sizeof(fr), "%f.2", ofGetFrameRate() );
    ofDrawBitmapString(fr, 20, 20);
    
    _img.draw(40, 40);
    

}





//--------------------------------------------------------------
void testApp::keyPressed(int key){

}

//--------------------------------------------------------------
void testApp::keyReleased(int key){

}

//--------------------------------------------------------------
void testApp::mouseMoved(int x, int y ){

}

//--------------------------------------------------------------
void testApp::mouseDragged(int x, int y, int button){

}

//--------------------------------------------------------------
void testApp::mousePressed(int x, int y, int button){

}

//--------------------------------------------------------------
void testApp::mouseReleased(int x, int y, int button){

}

//--------------------------------------------------------------
void testApp::windowResized(int w, int h){

}

//--------------------------------------------------------------
void testApp::gotMessage(ofMessage msg){

}

//--------------------------------------------------------------
void testApp::dragEvent(ofDragInfo dragInfo){ 

}
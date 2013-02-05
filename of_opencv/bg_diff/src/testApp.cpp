#include "testApp.h"

//--------------------------------------------------------------
void testApp::setup(){
    
    ofSetVerticalSync(true);
    ofSetFrameRate(60);
    
    _initRun = false;
    
    _width = 240;
    _height = 135;
    _learnRate = 0.75f;
    _threshold = 50;
    _requiredPctFill = 0.5f;
    
    _buffer.x = 40;
    _buffer.y = 40;
    
    _cam.initGrabber(_width, _height);
    _background.setLearningRate(_learnRate);
    _background.setThresholdValue(_threshold);
    
#if defined(WIN32) || defined(WIN64) || defined(__APPLE__)

    ofRectangle uiRect( _buffer.x,
                        _buffer.y * 3 + _height * 2,
                        _width,
                        _height );
    
    _gui = new ofxUICanvas(uiRect);

    ofSetWindowShape( (_width *2 + _buffer.x *3),
                     (_height *3 + _buffer.y *4) );
    
    _gui -> addSlider( "Threshold",    0.0f, 100.0f, _threshold,       _width - 10, 20);
    _gui -> addSlider( "Learn Rate",   0.0f, 1.0f,   _learnRate,       _width - 10, 20);
    _gui -> addSlider( "Rqd Max Fill", 0.0f, 1.0f,   _requiredPctFill, _width - 10, 20);
    
    ofAddListener( _gui->newGUIEvent, this, &testApp::guiEvent );
    
    _gui -> loadSettings("settings.xml");
    
#else
    
    ofSetWindowShape( (_width *2 + _buffer.x *3),
                     (_height *2 + _buffer.y *3) );
    
#endif
    
    
}

//--------------------------------------------------------------
void testApp::update() {
    _cam.update();
    
    if(_cam.isFrameNew()) {
        if( !_initRun ) {
            _initRun = true;
            _coloredImage = _cam.getPixelsRef();
            _coloredImage.update();
        }
        _background.update(_cam, _diff);
        _diff.update();
        
        calculateChanges();
    }
    
    ofxCv::toOf(_background.getBackground(), _bgImage);
    _bgImage.update();
    
}

//--------------------------------------------------------------
void testApp::calculateChanges() {
    unsigned char* colorPixels = _coloredImage.getPixels();
    unsigned char* diffPixels = _diff.getPixels();
    
    unsigned char red[3] = {255, 0, 0};
    unsigned char white[3] = {255, 255, 255};
    
    float reds = 0;
    float hits = 0;
    
    int depth = _coloredImage.bpp/8;
    for( int i = 0; i < _coloredImage.width * _coloredImage.height; ++i ) {
        
        int r = colorPixels[i*depth];
        int g = colorPixels[i*depth + 1];
        int b = colorPixels[i*depth + 2];
        
        if( memcmp(red, colorPixels + (i*depth), depth) == 0 ) {
         
            ++reds;
            
            unsigned int diffDepth = _diff.bpp/8;
            if( diffDepth == 1 ) {
                if( diffPixels[i] == 255 ) {
                    ++hits;
                }
            } else {
                if( memcmp(white, diffPixels + (i*diffDepth), sizeof(white)) == 0 ) {
                    ++hits;
                }
            }
        }
    }
    
    if( reds ) {
        if( hits/reds >= _requiredPctFill ) {
            char str[100];
            float pct = hits/reds;

            snprintf(str, sizeof(str), "We have a hit! Pct of %.3f", pct);
            ofLog(OF_LOG_NOTICE, str);
        }
    }
}

//--------------------------------------------------------------
void testApp::draw() {
	
    char fr[10];
    snprintf( fr, sizeof(fr), "%.2f", ofGetFrameRate() );
    ofDrawBitmapString(fr, _buffer/2);
    
    _cam.draw(_buffer);
    _bgImage.draw(_buffer.x * 2 + _width, _buffer.y);

    _diff.draw(_buffer.x, _buffer.y * 2 + _height);
    
    _coloredBounds = ofRectangle( _buffer.x * 2 + _width,
                                  _buffer.y * 2 + _height,
                                  _width,
                                  _height );
    
    _coloredImage.draw( _coloredBounds.x, _coloredBounds.y );
    
}

void testApp::guiEvent(ofxUIEventArgs& e)
{
    string name = e.widget->getName();
	int kind = e.widget->getKind();
	
    if( kind == OFX_UI_WIDGET_SLIDER_H ) {
        
        ofxUISlider* slider = (ofxUISlider *) e.widget;
        //cout << slider -> getIncrement() << endl;
        
        if( name == "Threshold" ) {
            _threshold = slider->getScaledValue();
            //cout << _threshold << endl;
            _background.setThresholdValue(_threshold);

        } else if ( name == "Learn Rate" ) {
            _learnRate = slider->getScaledValue();
            //cout << _learnRate << endl;
            _background.setLearningRate(_learnRate);
            
        }
    }
}

//--------------------------------------------------------------
void testApp::keyPressed(int key){

    if(key == ' ') {
        _coloredImage = _cam.getPixelsRef();
        _coloredImage.update();
        ofLog(OF_LOG_NOTICE, "Updated background for pixel draw");
    }
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
    
    _dragArea.x = x;
    _dragArea.y = y;
    
}

//--------------------------------------------------------------
void testApp::mouseReleased(int x, int y, int button){
   
    if( ! _coloredBounds.inside(x, y) ) { return; }
    if( ! _coloredBounds.inside(_dragArea.x, _dragArea.y) ) { return; }
    
    float centerX = (x + _dragArea.x)/2;
    float centerY = (y + _dragArea.y)/2;
    float width = abs(x - _dragArea.x);
    float height = abs(y - _dragArea.y);
    
    _dragArea.setFromCenter(centerX, centerY, width, height);
    
    unsigned char* pix = _coloredImage.getPixels();
    int depth = _coloredImage.bpp/8;
    
    for(int xx = _dragArea.getMinX(); xx < _dragArea.getMaxX(); ++xx) {
        for(int yy = _dragArea.getMinY(); yy < _dragArea.getMaxY(); ++yy) {
                        
            int index = ((yy - _coloredBounds.y) * _width) + ((int)(xx - _coloredBounds.x) % (int)_width);
            pix[index * depth] = 255;
            pix[index * depth + 1] = 0;
            pix[index * depth + 2] = 0;
            
        }
    }
    
    _coloredImage.update();
    
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

//--------------------------------------------------------------
void testApp::exit(){
    _gui -> saveSettings("settings.xml");
}
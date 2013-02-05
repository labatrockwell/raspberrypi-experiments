#pragma once

//#define RASP_ROLLOUT

#include "ofMain.h"
#include "ofxCv.h"

#include "ofxUI.h"


class testApp : public ofBaseApp{

public:
    void setup();
    void update();
    void draw();

    void keyPressed  (int key);
    void keyReleased(int key);
    void mouseMoved(int x, int y );
    void mouseDragged(int x, int y, int button);
    void mousePressed(int x, int y, int button);
    void mouseReleased(int x, int y, int button);
    void windowResized(int w, int h);
    void dragEvent(ofDragInfo dragInfo);
    void gotMessage(ofMessage msg);
    void exit();

    int                         _width;
    int                         _height;
    float                       _learnRate;
    float                       _threshold;
    float                       _requiredPctFill;
    ofVec2f                     _buffer;
    bool                        _initRun;
    
    ofVideoGrabber              _cam;
    ofxCv::RunningBackground    _background;
    ofImage                     _diff;
    ofImage                     _bgImage;
    ofImage                     _coloredImage;
    ofRectangle                 _coloredBounds;
    ofRectangle                 _dragArea;
    
    ofxUICanvas *               _gui;
    
    void guiEvent(ofxUIEventArgs& e);
    void calculateChanges();

    
};

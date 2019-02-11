//
//  GameViewController.swift
//  SlingRage
//
//  Created by Ratanaksamrith You on 7/9/15.
//  Copyright (c) 2015 Ratanaksamrith You. All rights reserved.
//

import UIKit
import SpriteKit

class GameViewController: UIViewController {

    override func viewDidLoad() {
        super.viewDidLoad()
        
        let skView = view as! SKView
        let skScene = GameScene(size: skView.bounds.size)
        skView.presentScene(skScene)
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Release any cached data, images, etc that aren't in use.
    }
}

//
//  GameScene.swift
//  SlingRage
//
//  Created by Ratanaksamrith You on 7/9/15.
//  Copyright (c) 2015 Ratanaksamrith You. All rights reserved.
//

import SpriteKit


let weapon = SKSpriteNode(imageNamed: "circle")
let enemy = SKSpriteNode(imageNamed: "enemy")
var touched = false
var beginTouchLocation = CGPoint()
var endTouchLocation = CGPoint()
var pathToDraw = CGMutablePath.init()
var line = SKShapeNode()

let wallCategory : UInt32 = 1
let weaponCategory : UInt32 = 2
let enemyCategory: UInt32 = 4

class GameScene: SKScene, SKPhysicsContactDelegate{
    override func didMove(to view: SKView) {
        /* Setup your scene here */
        
        // configure scene
        self.backgroundColor = UIColor(red: 0/255, green: 126/255, blue: 132/255, alpha: 1.0)
      self.physicsBody = SKPhysicsBody(edgeLoopFrom: self.frame)
        self.physicsWorld.gravity = CGVector(dx: 0, dy: 0)
        self.physicsWorld.contactDelegate = self
        
        // weapon node
        weapon.position = CGPoint(x: CGRectGetMidX(self.frame), y: 100)
        weapon.name = "weaponNode"
        weapon.physicsBody = SKPhysicsBody(circleOfRadius: weapon.size.width/2)
        weapon.physicsBody?.categoryBitMask = weaponCategory
        weapon.physicsBody?.contactTestBitMask = enemyCategory
        weapon.physicsBody?.friction = 0.0
        weapon.physicsBody?.restitution = 1
        weapon.physicsBody?.linearDamping = 1
        self.addChild(weapon)
        
        // enemy node
        enemy.position = CGPoint(x: CGRectGetMidX(self.frame), y: size.height - 200)
        enemy.name = "enemyNode"
        enemy.physicsBody = SKPhysicsBody(circleOfRadius: enemy.size.width/2)
        enemy.physicsBody?.categoryBitMask = enemyCategory
        self.addChild(enemy)

    }
    
    // remove enemyNode when contact weaponNode
    func didBeginContact(contact: SKPhysicsContact) {
        if contact.bodyA.categoryBitMask < contact.bodyB.categoryBitMask{
            contact.bodyB.node?.removeFromParent()
        }
    }
    
    override func touchesBegan(touches: Set<UITouch>, withEvent event: UIEvent?) {
       /* Called when a touch begins */
        touched = false
        for touch in touches {
            let touchedLocation = touch.locationInNode(self)
            let selectedNode = self.nodeAtPoint(touchedLocation)
            if selectedNode.name == "weaponNode" {
                touched = true
                weapon.physicsBody?.velocity = CGVector(dx: 0, dy: 0)
                beginTouchLocation = selectedNode.position
                line = SKShapeNode()
                self.addChild(line)
            }
            
        }

    }
    
  override func touchesMoved(_ touches: Set<UITouch>, with event: UIEvent?) {
        if touched == true {
            for touch in touches {
              let location = touch.location(in: self)
                endTouchLocation = CGPoint(x: location.x, y: location.y)
                
                
                // draw tracing straight line when drag weaponNode
              pathToDraw = CGMutablePath()
                
                // starting point
                CGPathMoveToPoint(pathToDraw, nil, beginTouchLocation.x, beginTouchLocation.y)
                
                // ending point
                weapon.position = endTouchLocation
                CGPathAddLineToPoint(pathToDraw, nil, weapon.position.x, weapon.position.y)
                
                line.path = pathToDraw
            }
        }

    }
    
    override func touchesEnded(touches: Set<UITouch>, withEvent event: UIEvent?) {
        if touched == true {
            line.removeFromParent()
            touched = false
            
            // calculate vector's magnitude to project weapon
            let slingVectorX = -CGFloat(weapon.position.x - beginTouchLocation.x)
            let slingVectorY = -CGFloat(weapon.position.y - beginTouchLocation.y)
            weapon.physicsBody?.applyImpulse(CGVector(dx: slingVectorX/2, dy: slingVectorY/2))
            
            // reset endTouchLocation
            endTouchLocation = CGPoint(x: 0, y: 0)

        } else {
            return
        }
    }
    
   
    override func update(currentTime: CFTimeInterval) {
        /* Called before each frame is rendered */
    }
}

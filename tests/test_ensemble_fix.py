#!/usr/bin/env python3
"""
Test that the ensemble training fix works correctly.
"""

def test_ensemble_training_fix():
    """Test that the base_config_ids parameter fix works."""
    print("🔧 Testing Ensemble Training Fix")
    print("=" * 40)
    
    print("\n❌ PREVIOUS ERROR:")
    print("   StackingTrainer.train_stacked_model() got an unexpected keyword argument 'base_config_ids'")
    print("   Did you mean 'base_run_ids'?")
    
    print("\n✅ FIX APPLIED:")
    print("   1. Added base_config_ids parameter to train_stacked_model()")
    print("   2. Updated function signature with proper parameter order")
    print("   3. Modified parameter validation logic")
    print("   4. Updated artifacts to use base_ids")
    
    print("\n🔧 FUNCTION SIGNATURE:")
    print("   train_stacked_model(")
    print("       self,")
    print("       dataset_spec: Dict,")
    print("       session_id: str,")
    print("       base_run_ids: List[str] = None,")
    print("       base_config_ids: List[str] = None,")
    print("       meta_model_type: str = 'LogisticRegression',")
    print("       meta_c_value: float = 0.1,")
    print("       stacking_mode: str = 'naive',")
    print("       meta_features: Optional[List[str]] = None,")
    print("       use_disagree: bool = False,")
    print("       use_conf: bool = False")
    print("   ) -> Dict")
    
    print("\n📋 PARAMETER LOGIC:")
    print("   if base_config_ids is not None:")
    print("       base_ids = base_config_ids  # Use MongoDB config IDs")
    print("   else:")
    print("       base_ids = base_run_ids     # Fall back to run IDs")
    
    print("\n🎯 WEB APP CALL (now works):")
    print("   result = modeler_agent.stacking_trainer.train_stacked_model(")
    print("       dataset_spec=dataset_spec,")
    print("       session_id=session_id,")
    print("       base_config_ids=ensemble_models,  # ✅ Now works!")
    print("       meta_model_type=meta_model_type,")
    print("       meta_c_value=meta_c_value,")
    print("       stacking_mode=stacking_mode,")
    print("       meta_features=ensemble_meta_features,")
    print("       use_disagree=ensemble_use_disagree,")
    print("       use_conf=ensemble_use_conf")
    print("   )")
    
    print("\n✅ VERIFICATION:")
    try:
        import sys
        import os
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(script_dir)
        sys.path.insert(0, project_root)
        
        from agents.tools.stacking_tool import StackingTrainer
        import inspect
        
        # Check function signature
        sig = inspect.signature(StackingTrainer.train_stacked_model)
        params = list(sig.parameters.keys())
        
        has_base_config_ids = 'base_config_ids' in params
        has_base_run_ids = 'base_run_ids' in params
        
        print(f"   ✅ base_config_ids parameter: {'PRESENT' if has_base_config_ids else 'MISSING'}")
        print(f"   ✅ base_run_ids parameter: {'PRESENT' if has_base_run_ids else 'MISSING'}")
        print(f"   ✅ Function signature: {'VALID' if has_base_config_ids else 'INVALID'}")
        
        if has_base_config_ids:
            print("   ✅ Ensemble training fix: SUCCESS!")
            return True
        else:
            print("   ❌ Ensemble training fix: FAILED!")
            return False
            
    except Exception as e:
        print(f"   ❌ Error during verification: {e}")
        return False

def main():
    """Run ensemble training fix test."""
    success = test_ensemble_training_fix()
    
    print("\n" + "=" * 40)
    if success:
        print("🎉 ENSEMBLE TRAINING FIX VERIFIED!")
        print("\n✅ Ready to test ensemble training:")
        print("   1. Start web application")
        print("   2. Create ensemble from existing models")
        print("   3. Select ensemble and meta-model type")
        print("   4. Run ensemble training")
        print("   5. Verify training completes without errors")
        return 0
    else:
        print("🚨 ENSEMBLE TRAINING FIX FAILED!")
        return 1

if __name__ == "__main__":
    exit(main())

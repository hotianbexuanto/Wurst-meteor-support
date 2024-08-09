import zipfile
import os
import sys
import requests
import shutil
import tempfile

def modify_file(file_path, search_text, replace_text):
    with open(file_path, 'r') as file:
        file_data = file.read()
    
    file_data = file_data.replace(search_text, replace_text)
    
    with open(file_path, 'w') as file:
        file.write(file_data)

def extract_zip(zip_file_path, extract_to):
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

def download_and_extract_zip(url, extract_to):
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            zip_file_path = os.path.join(temp_dir, "Wurst7-master.zip")
            
            # ダウンロードの処理
            print(f"Downloading from {url} to {zip_file_path}...")
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                with open(zip_file_path, 'wb') as f:
                    shutil.copyfileobj(response.raw, f)
                print(f"Extracting {zip_file_path} to {extract_to}...")
                extract_zip(zip_file_path, extract_to)
                print("Extraction completed!")
            else:
                print(f"Failed to download file: {response.status_code}")
                sys.exit(1)
                
    except Exception as e:
        print(f"An error occurred during download and extraction: {e}")
        sys.exit(1)

def main():
    extract_to = os.path.join(os.getcwd(), "Wurst7-master")
    url = "https://github.com/Wurst-Imperium/Wurst7/archive/refs/heads/master.zip"
    
    download_and_extract_zip(url, extract_to)

    # 解凍されたファイルの構造を確認
    print("Directory structure after extraction:")
    for root, dirs, files in os.walk(extract_to):
        level = root.replace(extract_to, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print('{}{}/'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print('{}{}'.format(subindent, f))

    search_replace_list = [
        # fabric.mod.json
        ('src/main/resources/fabric.mod.json', '"id": "wurst"', '"id": "wurst-meteor"'),

        # GameRendererMixin
        ('src/main/java/net/wurstclient/mixin/GameRendererMixin.java', '\n\t@Redirect(\n\t\tat = @At(value = "INVOKE",\n\t\t\ttarget = "Lnet/minecraft/util/math/MathHelper;lerp(FFF)F",\n\t\t\tordinal = 0),\n\t\tmethod = "renderWorld(FJLnet/minecraft/client/util/math/MatrixStack;)V")\n\tprivate float wurstNauseaLerp(float delta, float start, float end)\n\t{\n\t\tif(!WurstClient.INSTANCE.getHax().antiWobbleHack.isEnabled())\n\t\t\treturn MathHelper.lerp(delta, start, end);\n\t\t\n\t\treturn 0;\n\t}\n\t', ''),
        
        # ClientPlayerEntitiyMixin
        ('src/main/java/net/wurstclient/mixin/ClientPlayerEntityMixin.java', 'import net.wurstclient.events.IsPlayerInLavaListener.IsPlayerInLavaEvent;', ''),
        ('src/main/java/net/wurstclient/mixin/ClientPlayerEntityMixin.java', '\n\t@Override\n\tpublic boolean isInLava()\n\t{\n\t\tboolean inLava = super.isInLava();\n\t\tIsPlayerInLavaEvent event = new IsPlayerInLavaEvent(inLava);\n\t\tEventManager.fire(event);\n\t\t\n\t\treturn event.isInLava();\n\t}\n\t\n\t@Override\n\tpublic boolean isSpectator()\n\t{\n\t\treturn super.isSpectator()\n\t\t\t|| WurstClient.INSTANCE.getHax().freecamHack.isEnabled();\n\t}\n\t', ''),
        
        # CameraMixin
        ('src/main/java/net/wurstclient/mixin/CameraMixin.java', 'import org.spongepowered.asm.mixin.injection.ModifyVariable;', ''),
        ('src/main/java/net/wurstclient/mixin/CameraMixin.java', 'import net.wurstclient.hacks.CameraDistanceHack;', ''),
        ('src/main/java/net/wurstclient/mixin/CameraMixin.java', '\n\t@ModifyVariable(at = @At("HEAD"),\n\t\tmethod = "clipToSpace(F)F",\n\t\targsOnly = true)\n\tprivate float changeClipToSpaceDistance(float desiredCameraDistance)\n\t{\n\t\tCameraDistanceHack cameraDistance =\n\t\t\tWurstClient.INSTANCE.getHax().cameraDistanceHack;\n\t\tif(cameraDistance.isEnabled())\n\t\t\treturn cameraDistance.getDistance();\n\t\t\n\t\treturn desiredCameraDistance;\n\t}\n\t', ''),
        
        # BlockMixin
        ('src/main/java/net/wurstclient/mixin/BlockMixin.java', '\n\t\n\t@Inject(at = @At("HEAD"),\n\t\tmethod = "getVelocityMultiplier()F",\n\t\tcancellable = true)\n\tprivate void onGetVelocityMultiplier(CallbackInfoReturnable<Float> cir)\n\t{\n\t\tHackList hax = WurstClient.INSTANCE.getHax();\n\t\tif(hax == null || !hax.noSlowdownHack.isEnabled())\n\t\t\treturn;\n\t\t\n\t\tif(cir.getReturnValueF() < 1)\n\t\t\tcir.setReturnValue(1F);\n\t}', ''),
        
        # FilterShulkerBulletSetting
        ('src/main/java/net/wurstclient/hacks/ProtectHack.java', 'FilterShulkerBulletSetting.genericCombat(false),', ''),
        ('src/main/java/net/wurstclient/hacks/KillauraLegitHack.java', 'FilterShulkerBulletSetting.genericCombat(false),', ''),
        ('src/main/java/net/wurstclient/hacks/AimAssistHack.java', 'FilterShulkerBulletSetting.genericCombat(false),', ''),
        ('src/main/java/net/wurstclient/settings/filterlists/EntityFilterList.java', 'FilterShulkerBulletSetting.genericCombat(false),', ''),
        
        # Freecam
        ('src/main/java/net/wurstclient/hacks/FreecamHack.java', 'IsPlayerInLavaListener, CameraTransformViewBobbingListener,', 'PlayerMoveListener, CameraTransformViewBobbingListener,'),
        ('src/main/java/net/wurstclient/hacks/FreecamHack.java', 'EVENTS.add(IsPlayerInLavaListener.class, this);', 'EVENTS.add(PlayerMoveListener.class, this);'),
        ('src/main/java/net/wurstclient/hacks/FreecamHack.java', 'EVENTS.remove(IsPlayerInLavaListener.class, this);', 'EVENTS.remove(PlayerMoveListener.class, this);'),
        ('src/main/java/net/wurstclient/hacks/FreecamHack.java', '@Override\n\tpublic void onIsPlayerInLava(IsPlayerInLavaEvent event)\n\t{\n\t\tevent.setInLava(false);\n\t}', ''),             # Remove onIsPlayerInLava
        ('src/main/java/net/wurstclient/hacks/FreecamHack.java', 'GL11.glDisable(GL11.GL_BLEND);\n\t}\n}', 'GL11.glDisable(GL11.GL_BLEND);\n\t}\n\t@Override\n\tpublic void onPlayerMove() {}\n}'),  # Add  P.S. Not work BRO   PLEASE SELF FIX
    ]
    
    # Modify files
    for file_path, search_text, replace_text in search_replace_list:
        file_path = os.path.join(extract_to, "Wurst7-master", file_path)
        if os.path.isfile(file_path):
            modify_file(file_path, search_text, replace_text)
        else:
            print(f"File not found: {file_path}")
    
    print("Modification completed successfully!")
    print("Build it yourself!")
    print("Build Tutorial:\n1: Open the folder with gradlew.bat\n2: Open cmd type 'gradlew.bat :spotlessApply' and 'gradlew.bat build'")
    input("Press Enter to exit")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

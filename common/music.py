"""Camera library for scripts.
"""

import re
import sys
from common import Common

class Music(Common):
        
    def enter(self):
        """Launch music by StartActivity.
        """          
        self.logger.debug('enter music')
        if self.device(resourceId="com.alcatel.music5:id/action_search").wait.exists(timeout = 5000):
            return True
        self.start_app("Mix",b_desk=False)
        if self.device(resourceId="com.alcatel.music5:id/action_search").wait.exists(timeout = 5000):
            return True
        else:
            self.logger.warning('enter music fail!')
            return False
    
    def enter_library(self):
        self.logger.debug("Enter the music library")
        if self.device(description="Open navigation drawer").exists:
            self.device(description="Open navigation drawer").click()
        if self.device(resourceId="com.alcatel.music5:id/navigation_drawer").exists:
            self.device(text=self.appconfig("Music","library")).click()
            if self.device(resourceId="com.alcatel.music5:id/shuffle_all_btn").wait.exists(timeout = self.timeout):
                return True
        self.logger.warning("Cannot enter the library")
        return False

    def play(self,Index=0):
        """paly music 
        """
        self.logger.debug('play music')

        music_num = self.device(resourceId="com.alcatel.music5:id/item_recycler_parent_view").count
        music_index = Index % music_num + 1
        music_name = self.device(resourceId="com.alcatel.music5:id/recycler_view").child(resourceId="com.alcatel.music5:id/item_recycler_parent_view",index=music_index).child(resourceId="com.alcatel.music5:id/title_text_view").get_text()
        self.device(resourceId="com.alcatel.music5:id/recycler_view").child(resourceId="com.alcatel.music5:id/item_recycler_parent_view",index=music_index).click()
        self.device.delay(5)
        playing_name = self.device(resourceId="com.alcatel.music5:id/sliding_up_content_container").child(resourceId="com.alcatel.music5:id/title_text_view").get_text()
        if music_name == playing_name:
            self.logger.debug("Playing: %s" %music_name)
            self.device.delay(10)
            return True
        else:
            self.logger.debug("play music fail: %s" %music_name)
            return False

    def _exit(self):
        """exit music 
        """
        self.back_to_home()
        if self.device(packageName = self.appconfig("Music","package")).wait.gone(timeout = self.timeout):
            return True
        return False
    
    def is_playing_music(self):
        """check if music is playing or not.
        """
        data = self.device.server.adb.shell("dumpsys media_session")
        if not data:
            return None
        if "state=PlaybackState {state=3" in data:
            self.logger.debug("The music is playing now")
            return True
        else:
            self.logger.debug("The music is not playing.")
            return False

    def close(self):
        """close music 
        """
        self.logger.debug('close music')
        if self.is_playing_music():
            self.logger.debug('Stop music play')
            self.device(resourceId="com.alcatel.music5:id/track_play_pause_image_btn").click()
            self.device.delay(2)
        return self._exit()

if __name__ == '__main__':
    pass
            
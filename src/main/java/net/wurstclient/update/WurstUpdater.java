/*
 * Copyright (c) 2014-2024 Wurst-Imperium and contributors.
 *
 * This source code is subject to the terms of the GNU General Public
 * License, version 3. If a copy of the GPL was not distributed with this
 * file, You can obtain one at: https://www.gnu.org/licenses/gpl-3.0.txt
 */
package net.wurstclient.update;

import net.minecraft.text.ClickEvent;
import net.minecraft.text.Text;
import net.wurstclient.WurstClient;
import net.wurstclient.events.UpdateListener;
import net.wurstclient.util.ChatUtils;
import net.wurstclient.util.json.JsonException;
import net.wurstclient.util.json.WsonArray;
import net.wurstclient.util.json.WsonObject;

public final class WurstUpdater implements UpdateListener
{
	private Thread thread;
	private boolean outdated;
	private Text component;
	
	@Override
	public void onUpdate()
	{
		if(thread == null)
		{
			thread = new Thread(this::checkForUpdates, "WurstUpdater");
			thread.start();
			return;
		}
		
		if(thread.isAlive())
			return;
		
		if(component != null)
			ChatUtils.component(component);
		
		WurstClient.INSTANCE.getEventManager().remove(UpdateListener.class,
			this);
	}
	
	public void checkForUpdates()
	{
		return;
	}
	
	private void showLink(String text, String url)
	{
		ClickEvent event = new ClickEvent(ClickEvent.Action.OPEN_URL, url);
		component = Text.literal(text).styled(s -> s.withClickEvent(event));
	}
	
	private boolean containsCompatibleAsset(WsonArray wsonArray)
		throws JsonException
	{
		String compatibleSuffix = "MC" + WurstClient.MC_VERSION + ".jar";
		
		for(WsonObject asset : wsonArray.getAllObjects())
		{
			String assetName = asset.getString("name");
			if(!assetName.endsWith(compatibleSuffix))
				continue;
			
			return true;
		}
		
		return false;
	}
	
	public boolean isOutdated()
	{
		return outdated;
	}
}

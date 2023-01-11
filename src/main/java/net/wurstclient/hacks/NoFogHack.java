package net.wurstclient.hacks;

import net.wurstclient.Category;
import net.wurstclient.SearchTags;
import net.wurstclient.hack.Hack;

@SearchTags({"no fog", "NoFogOverlay"})
public final class NoFogHack extends Hack
{
    public NoFogHack()
    {
        super("NoFog");
        setCategory(Category.RENDER);
    }
}
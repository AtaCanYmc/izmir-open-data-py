"""
MCP (Model Context Protocol) Sunucusu Kullanım Örneği

MCP sunucusu, AI asistanlarının (örneğin Claude Desktop veya Cursor) 
İzmir Açık Veri API'sinden doğrudan veri çekmesine olanak tanır.

Normalde, MCP sunucusunu doğrudan CLI komutu ile çalıştırırsınız:
$ izmir-mcp

Eğer FastMCP sunucusunu kendi projenizde genişletmek veya 
özel araçlar (tools) eklemek isterseniz aşağıdaki gibi yapabilirsiniz.
"""

from src.izmir_open_data.mcp import mcp


# Mevcut MCP sunucusuna yeni, özel bir araç (tool) ekleyelim
@mcp.tool()
async def get_system_status() -> str:
    """
    Sistemin durumunu döndüren özel bir test aracı.
    AI asistanları bu aracı da keşfedip kullanabilir.
    """
    return "Sistem aktif ve İzmir Açık Veri API'sine bağlanmaya hazır."


if __name__ == "__main__":
    print("İzmir Açık Veri MCP Sunucusu (Özel Eklentilerle) Başlatılıyor...")
    # Sunucu standart girdi/çıktı (stdio) üzerinden çalışmaya başlar
    # Bu script AI asistanının konfigürasyonuna eklenebilir.
    mcp.run()

# NOT: MCP sunucusunu yerel olarak test etmek için resmi MCP Inspector'ı kullanabilirsiniz:
# npx @modelcontextprotocol/inspector uv run python examples/mcp_example.py

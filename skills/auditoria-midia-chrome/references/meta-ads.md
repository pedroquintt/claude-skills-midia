# Meta Ads e Events Manager

> Este roteiro ainda não foi validado numa sessão real. Na primeira auditoria Meta, corrija esta página com o que funcionar de verdade (URLs, seletores, armadilhas).

## URLs
- Gerenciador de Anúncios: `https://adsmanager.facebook.com/adsmanager/manage/campaigns?act=<ad_account_id>`
- Events Manager: `https://business.facebook.com/events_manager2/list/pixel/<pixel_id>/overview`
- Configurações do Business: `https://business.facebook.com/settings/`

Pegue o `act` e os pixel IDs pela URL ou pelo seletor de contas. Não presuma.

## Leitura
- O Ads Manager também virtualiza tabelas. Use JS com `[role="row"]`, ajuste "Colunas" para Desempenho e cliques e fixe o período em "Últimos 30 dias".
- Mostre a coluna de resultados **e** a de eventos específicos (Lead, Purchase): "Resultados" muda conforme o objetivo da campanha.

## Checklist
1. **Pixels no site**: quantos carregam (`connect.facebook.net/signals/config/<id>` nos scripts)? Mais de um pixel com o mesmo evento infla resultados se o Ads usar os dois.
2. **CAPI e deduplicação**: no Events Manager › Visão geral, cada evento deve mostrar "Navegador" e "Servidor" com deduplicação. O `event_id` precisa bater entre o pixel e o servidor (no GTM, procure a variável "Unique Event ID" ou "Get_Event_ID").
3. **Qualidade da correspondência do evento** (EMQ) por evento: nota baixa indica falta de e-mail ou telefone, ou de fbc/fbp.
4. **Evento de otimização** de cada conjunto × evento que realmente dispara no site. Lead otimizado num evento que dispara no clique (e não no envio) gera lead ruim.
5. **Eventos disparados por gambiarra** (ex.: `lead_confirmado` só no 2º envio de formulário). Entenda a regra antes de mexer.
6. **Domínio verificado** e **Configuração de eventos agregados** (impacto em iOS).
7. **Campanhas**: frequência, CPM, CTR do link, custo por resultado, fadiga de criativo (queda de CTR com frequência subindo), sobreposição de público.

## Mudanças (só com aprovação)
- Edição de campanhas, conjuntos, orçamentos e eventos de otimização pode ser bloqueada pela política do agente. Nesse caso, passe o caminho exato.
- Nunca altere configurações de domínio, pixel compartilhado ou acesso do Business sem pedido explícito.

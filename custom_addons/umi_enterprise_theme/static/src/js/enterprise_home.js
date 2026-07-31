import { registry } from "@web/core/registry";
import { Component, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { WebClient } from "@web/webclient/webclient";
import { NavBar } from "@web/webclient/navbar/navbar";
import { patch } from "@web/core/utils/patch";

export class EnterpriseHomeDashboard extends Component {
    static template = "umi_enterprise_theme.EnterpriseHomeDashboard";

    setup() {
        this.menuService = useService("menu");
        this.actionService = useService("action");
        this.state = useState({ searchQuery: "" });
    }

    get apps() {
        const query = this.state.searchQuery.trim().toLowerCase();
        const allApps = this.menuService.getApps();
        if (!query) {
            return allApps;
        }
        return allApps.filter((app) => app.name.toLowerCase().includes(query));
    }

    getAppIconUrl(app) {
        if (app.webIconData) {
            return app.webIconData;
        }
        if (app.webIcon) {
            const parts = app.webIcon.split(",");
            if (parts.length >= 2) {
                return `/${parts[0].trim()}/${parts[1].trim()}`;
            }
            return `/${app.webIcon.trim()}`;
        }
        return false;
    }

    async selectApp(app) {
        await this.menuService.selectMenu(app);
    }
}

registry.category("actions").add("umi_enterprise_home", EnterpriseHomeDashboard);

// Patch WebClient to open EnterpriseHomeDashboard on login / default app load
patch(WebClient.prototype, {
    async _loadDefaultApp() {
        try {
            await this.actionService.doAction("umi_enterprise_theme.action_enterprise_home", { clearBreadcrumbs: true });
        } catch (e) {
            console.error("Error launching Enterprise Home:", e);
            super._loadDefaultApp();
        }
    },
});

// Patch NavBar to open EnterpriseHomeDashboard when top-left menu icon is clicked
patch(NavBar.prototype, {
    onAllAppsBtnClick() {
        return this.actionService.doAction("umi_enterprise_theme.action_enterprise_home", { clearBreadcrumbs: true });
    },
});

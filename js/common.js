/**
 * Common header and footer templates for Plants vs Brainrots Codes website
 * This file ensures consistency across all pages
 */

// Common navigation header HTML template
const getCommonHeader = (activePage = '') => {
    return `
    <nav class="navbar">
        <div class="container">
            <div class="nav-brand">
                <a href="/">Plants vs Brainrots Codes</a>
            </div>
            <button class="nav-toggle" aria-label="Toggle navigation">
                <span></span>
                <span></span>
                <span></span>
            </button>
            <ul class="nav-menu">
                <li><a href="/" ${activePage === 'index' ? 'class="active"' : ''}>Home</a></li>
                <li><a href="/codes" ${activePage === 'codes' ? 'class="active"' : ''}>Codes</a></li>
                <li><a href="/gameplay" ${activePage === 'gameplay' ? 'class="active"' : ''}>How to Play</a></li>
                <li><a href="/plants" ${activePage === 'plants' ? 'class="active"' : ''}>Plants</a></li>
                <li><a href="/brainrots" ${activePage === 'brainrots' ? 'class="active"' : ''}>Brainrots</a></li>
                <li><a href="/bosses" ${activePage === 'bosses' ? 'class="active"' : ''}>Bosses</a></li>
                <li><a href="/fusion" ${activePage === 'fusion' ? 'class="active"' : ''}>Fusion</a></li>
                <li><a href="/rebirth" ${activePage === 'rebirth' ? 'class="active"' : ''}>Rebirth</a></li>
            </ul>
        </div>
    </nav>`;
};

// Common footer HTML template
const getCommonFooter = () => {
    return `
    <footer>
        <div class="container">
            <div class="footer-content">
                <div class="footer-section">
                    <h4>Quick Links</h4>
                    <ul>
                        <li><a href="/codes">Latest Codes</a></li>
                        <li><a href="/gameplay">How to Play</a></li>
                        <li><a href="/gameplay#beginner">Beginner's Guide</a></li>
                        <li><a href="https://www.roblox.com/games/127742093697776/Plants-Vs-Brainrots" target="_blank" rel="noopener">Play Game</a></li>
                    </ul>
                </div>
                <div class="footer-section">
                    <h4>Game Guides</h4>
                    <ul>
                        <li><a href="/plants">All Plants</a></li>
                        <li><a href="/brainrots">All Brainrots</a></li>
                        <li><a href="/bosses">Boss Strategies</a></li>
                        <li><a href="/fusion">Fusion Recipes</a></li>
                    </ul>
                </div>
                <div class="footer-section">
                    <h4>Game Systems</h4>
                    <ul>
                        <li><a href="/rebirth">Rebirth Guide</a></li>
                        <li><a href="/brainrots#income">Income Strategy</a></li>
                        <li><a href="/gameplay#tips">Tips & Tricks</a></li>
                        <li><a href="/codes#how-to-redeem">Redeem Codes</a></li>
                    </ul>
                </div>
                <div class="footer-section">
                    <h4>Community</h4>
                    <ul>
                        <li><a href="https://discord.gg/plantsvbrainrots" target="_blank" rel="noopener">Discord Server</a></li>
                        <li><a href="https://twitter.com/plantsvbrainrots" target="_blank" rel="noopener">Twitter</a></li>
                        <li><a href="/index#about">About Us</a></li>
                        <li><a href="/index#contact">Contact</a></li>
                    </ul>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; 2024 PlantsVsBrainrotsCodes.com - Not affiliated with Yo Gurt Studio or Roblox Corporation</p>
            </div>
        </div>
    </footer>`;
};

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { getCommonHeader, getCommonFooter };
}

// For use in browser
window.siteTemplates = {
    getCommonHeader,
    getCommonFooter
};
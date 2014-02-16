import sublime
import sublime_plugin

class PaneCommand(sublime_plugin.WindowCommand):
    """Base class."""

     ######  ##    ##  ######  ##       ########
    ##    ##  ##  ##  ##    ## ##       ##
    ##         ####   ##       ##       ##
    ##          ##    ##       ##       ######
    ##          ##    ##       ##       ##
    ##    ##    ##    ##    ## ##       ##
     ######     ##     ######  ######## ########

    def cycle(self, direction):
        if direction == 'next':
            self.goto(self.next_pane())
        elif direction == 'prev':
            self.goto(self.prev_pane())

    def goto(self, pane):
        self.window.focus_group(pane)

    def next_pane(self):
        target = self.window.active_group() + 1
        last_pane = self.window.num_groups() - 1
        if target > last_pane:
            return 0
        else:
            return target

    def prev_pane(self):
        target = self.window.active_group() - 1
        last_pane = self.window.num_groups() - 1
        if target < 0:
            return last_pane
        else:
            return target

    ########  ########  ######  #### ######## ########
    ##     ## ##       ##    ##  ##       ##  ##
    ##     ## ##       ##        ##      ##   ##
    ########  ######    ######   ##     ##    ######
    ##   ##   ##             ##  ##    ##     ##
    ##    ##  ##       ##    ##  ##   ##      ##
    ##     ## ########  ######  #### ######## ########

    def expand(self):
        layout = self.window.get_layout()
        cells = layout['cells']
        rows = layout['rows']
        cols = layout['cols']

        if len(cells) < 2:
            return

        pane = self.window.active_group()

        layout = self.push_left(layout, pane, self.amount)
        layout = self.push_right(layout, pane, self.amount)

        i = pane
        x = self.amount
        while i > 1:
            i -= 1
            x -= (self.amount/pane)
            layout = self.push_left(layout, i, x)

        i = pane
        x = self.amount
        end = len(cols) - 2
        while i < end:
            i += 1
            x -= (self.amount/(end-pane))
            layout = self.push_right(layout, i, x)

        self.window.set_layout(layout)

    def push_left(self, layout, pane, amount):
        cells = layout['cells']
        rows = layout['rows']
        cols = layout['cols']

        # Left
        if cols[cells[pane][0]] != 0:
            cols[cells[pane][0]] = max(cols[cells[pane][0]] - amount, 0 + self.padding)
        # Top
        if rows[cells[pane][1]] != 0:
            rows[cells[pane][1]] = max(rows[cells[pane][1]] - amount, 0 + self.padding)

        return layout

    def push_right(self, layout, pane, amount):
        cells = layout['cells']
        rows = layout['rows']
        cols = layout['cols']

        # Right
        if cols[cells[pane][2]] != 1:
            cols[cells[pane][2]] = min(cols[cells[pane][2]] + amount, 1 - self.padding)
        # Bottom
        if rows[cells[pane][3]] != 1:
            rows[cells[pane][3]] = min(rows[cells[pane][3]] + amount, 1 - self.padding)

        return layout

    def contract(self):
        layout = self.window.get_layout()
        cells = layout['cells']
        rows = layout['rows']
        cols = layout['cols']

        if len(cells) < 2:
            return

        pane = self.window.active_group()


        layout = self.pull_left(layout, pane, self.amount)
        layout = self.pull_right(layout, pane, self.amount)

        i = pane
        x = self.amount
        while i > 1:
            i -= 1
            x -= (self.amount/pane)
            layout = self.pull_left(layout, i, x)

        i = pane
        x = self.amount
        end = len(cols) - 2
        while i < end:
            i += 1
            x -= (self.amount/(end-pane))
            layout = self.pull_right(layout, i, x)

        self.window.set_layout(layout)

    def pull_left(self, layout, pane, amount):
        cells = layout['cells']
        rows = layout['rows']
        cols = layout['cols']

        # Left
        if cols[cells[pane][0]] != 0:
            cols[cells[pane][0]] = min(cols[cells[pane][0]] + amount, 1 - self.padding)
        # Top
        if rows[cells[pane][1]] != 0:
            rows[cells[pane][1]] = min(rows[cells[pane][1]] + amount, 1 - self.padding)

        return layout

    def pull_right(self, layout, pane, amount):
        cells = layout['cells']
        rows = layout['rows']
        cols = layout['cols']

        # Right
        if cols[cells[pane][2]] != 1:
            cols[cells[pane][2]] = max(cols[cells[pane][2]] - amount, 0 + self.padding)
        # Bottom
        if rows[cells[pane][3]] != 1:
            rows[cells[pane][3]] = max(rows[cells[pane][3]] - amount, 0 + self.padding)

        return layout


class CyclePane(PaneCommand):
    def run(self, direction):
        self.cycle(direction)


class ResizePane(PaneCommand):
    def run(self, direction):
        settings = sublime.load_settings('Pane Resizer.sublime-settings')
        self.amount = settings.get('resize_amount')
        self.padding = max(settings.get('padding'), 0.00001)

        if direction == 'out':
            self.expand()
        elif direction == 'in':
            self.contract()

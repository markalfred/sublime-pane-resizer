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


class CyclePane(PaneCommand):
    def run(self, direction):
        self.cycle(direction)

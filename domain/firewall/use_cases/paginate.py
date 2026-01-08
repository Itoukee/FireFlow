from domain.firewall.repository import FirewallRepository


class PaginateFirewallsUC:
    def __init__(self, repo: FirewallRepository) -> None:
        self.repo = repo

    def execute(self, page: int, limit: int):
        return self.repo.paginate(page, limit)

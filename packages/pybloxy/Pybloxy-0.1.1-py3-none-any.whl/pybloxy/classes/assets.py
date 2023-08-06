from .http import Http
import json

class Asset:
    Name = None
    Id = None
    ProductId = None
    Description = None
    AssetTypeId = None
    CreatorName = None
    CreatorId = None
    CreatorTargetId = None
    IconImageAssetId = None
    Created = None
    Updated = None
    PriceInRobux = None
    Sales = None
    IsNew = None
    IsForSale = None
    IsPublicDomain = None
    IsLimited = None
    IsLimitedUnique = None
    Remaining = None
    MinimumMembershipLevel = None
    ContentRatingTypeId = None

    def __init__(self, data):
        self.Name = data["Name"]
        self.Id = data["AssetId"]
        self.ProductId = data["ProductId"]
        self.Description = data["Description"]
        self.AssetTypeId = data["AssetTypeId"]
        self.CreatorName = data["Creator"]["Name"]
        self.CreatorId = data["Creator"]["Id"]
        self.CreatorType = data["Creator"]["CreatorType"]
        self.CreatorTargetId = data["Creator"]["CreatorTargetId"]
        self.IconImageAssetId = data["IconImageAssetId"]
        self.Created = data["Created"]
        self.Updated = data["Updated"]
        self.PriceInRobux = data["PriceInRobux"]
        self.Sales = data["Sales"]
        self.IsNew = data["IsNew"]
        self.IsForSale = data["IsForSale"]
        self.IsPublicDomain = data["IsPublicDomain"]
        self.IsLimited = data["IsLimited"]
        self.IsLimitedUnique = data["IsLimitedUnique"]
        self.Remaining = data["Remaining"]
        self.MinimumMembershipLevel = data["MinimumMembershipLevel"]
        self.ContentRatingTypeId = data["ContentRatingTypeId"]


class Assets:
    def getPackageAsset(assetid):
        res = Http.sendRequest(
            "https://www.roblox.com/Game/GetAssetIdsForPackageId?packageId=" +
            str(assetid))

        result = []

        for part in res:
            i = res.index(part)
            link = "https://www.roblox.com/library/" + str(part)
            result.insert(i, link)
        return result

    def hasAsset(userid, assetid):
        res = Http.sendRequest(
            "https://api.roblox.com/Ownership/HasAsset?userId=" + str(userid) +
            "&assetId=" + str(assetid))

        if res == "true" or True:
            return True
        else:
            return False

    def asset(assetid):
        res = Http.sendRequest(
            "https://api.roblox.com/Marketplace/ProductInfo?assetId=" +
            str(assetid))
        res_decoded = res.decode("utf-8")
        res_loads = json.loads(res_decoded)
        return Asset(res_loads)

    def assetVersions(assetid):
        res = Http.sendRequest(
            "https://www.roblox.com/studio/plugins/info?assetId=" +
            str(assetid))

        result = []

        for part in res:
            i = res.index(part)
            result.insert(i, part)

        return result

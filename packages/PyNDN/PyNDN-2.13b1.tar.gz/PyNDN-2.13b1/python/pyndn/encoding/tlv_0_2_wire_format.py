# -*- Mode:python; c-file-style:"gnu"; indent-tabs-mode:nil -*- */
#
# Copyright (C) 2014-2021 Regents of the University of California.
# Author: Jeff Thompson <jefft0@remap.ucla.edu>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# A copy of the GNU Lesser General Public License is in the file COPYING.

from random import SystemRandom
from pyndn.util.blob import Blob
from pyndn.encoding.tlv_0_3_wire_format import Tlv0_3WireFormat
from pyndn.encoding.tlv.tlv_encoder import TlvEncoder
from pyndn.encoding.tlv.tlv import Tlv
haveModule_pyndn = True
try:
    import _pyndn
except ImportError:
    haveModule_pyndn = False

# The Python documentation says "Use SystemRandom if you require a
#   cryptographically secure pseudo-random number generator."
# http://docs.python.org/2/library/random.html
_systemRandom = SystemRandom()

"""
This module defines the Tlv0_2WireFormat class which extends WireFormat to
override its methods to implment encoding and decoding Interest, Data, etc.
with the NDN-TLV wire format, version 0.2.
"""

class Tlv0_2WireFormat(Tlv0_3WireFormat):
    _instance = None

    def encodeInterest(self, interest):
        """
        Encode interest in NDN-TLV and return the encoding.

        :param Interest interest: The Interest object to encode.
        :return: A Tuple of (encoding, signedPortionBeginOffset,
          signedPortionEndOffset) where encoding is a Blob containing the
          encoding, signedPortionBeginOffset is the offset in the encoding of
          the beginning of the signed portion, and signedPortionEndOffset is
          the offset in the encoding of the end of the signed portion. The
          signed portion starts from the first name component and ends just
          before the final name component (which is assumed to be a signature
          for a signed interest).
        :rtype: (Blob, int, int)
        """
        if not interest._didSetCanBePrefix and not Tlv0_3WireFormat._didCanBePrefixWarning:
            print(
              "WARNING: The default CanBePrefix will change. See Interest.setDefaultCanBePrefix() for details.")
            Tlv0_3WireFormat._didCanBePrefixWarning = True

        if haveModule_pyndn:
            # Use the C bindings.
            result = _pyndn.Tlv0_2WireFormat_encodeInterest(interest)
            return (Blob(result[0], False), result[1], result[2])

        if interest.hasApplicationParameters():
            # The application has specified a format v0.3 field. As we
            # transition to format v0.3, encode as format v0.3 even though the
            # application default is Tlv0_2WireFormat.
            return self._encodeInterestV03(interest)

        encoder = TlvEncoder(256)
        saveLength = len(encoder)

        # Encode backwards.
        if interest.getForwardingHint().size() > 0:
            if interest.getSelectedDelegationIndex() != None:
                raise RuntimeError(
                  "An Interest may not have a selected delegation when encoding a forwarding hint")
            if interest.hasLink():
                raise RuntimeError(
                  "An Interest may not have a link object when encoding a forwarding hint")

            forwardingHintSaveLength = len(encoder)
            Tlv0_3WireFormat._encodeDelegationSet(
              interest.getForwardingHint(), encoder)
            encoder.writeTypeAndLength(
              Tlv.ForwardingHint, len(encoder) - forwardingHintSaveLength)

        encoder.writeOptionalNonNegativeIntegerTlv(
          Tlv.SelectedDelegation, interest.getSelectedDelegationIndex())
        linkWireEncoding = interest.getLinkWireEncoding(self)
        if not linkWireEncoding.isNull():
          # Encode the entire link as is.
          encoder.writeBuffer(linkWireEncoding.buf())

        encoder.writeOptionalNonNegativeIntegerTlvFromFloat(
          Tlv.InterestLifetime, interest.getInterestLifetimeMilliseconds())

        # Encode the Nonce as 4 bytes.
        if interest.getNonce().size() == 0:
            # This is the most common case. Generate a nonce.
            nonce = bytearray(4)
            for i in range(4):
                nonce[i] = _systemRandom.randint(0, 0xff)
            encoder.writeBlobTlv(Tlv.Nonce, nonce)
        elif interest.getNonce().size() < 4:
            nonce = bytearray(4)
            # Copy existing nonce bytes.
            nonce[:interest.getNonce().size()] = interest.getNonce().buf()

            # Generate random bytes for remaining bytes in the nonce.
            for i in range(interest.getNonce().size(), 4):
                nonce[i] = _systemRandom.randint(0, 0xff)

            encoder.writeBlobTlv(Tlv.Nonce, nonce)
        elif interest.getNonce().size() == 4:
            # Use the nonce as-is.
            encoder.writeBlobTlv(Tlv.Nonce, interest.getNonce().buf())
        else:
            # Truncate.
            encoder.writeBlobTlv(Tlv.Nonce, interest.getNonce().buf()[:4])

        self._encodeSelectors(interest, encoder)

        (tempSignedPortionBeginOffset, tempSignedPortionEndOffset) = \
          self._encodeName(interest.getName(), encoder)
        signedPortionBeginOffsetFromBack = (len(encoder) -
                                            tempSignedPortionBeginOffset)
        signedPortionEndOffsetFromBack = (len(encoder) -
                                          tempSignedPortionEndOffset)

        encoder.writeTypeAndLength(Tlv.Interest, len(encoder) - saveLength)
        signedPortionBeginOffset = (len(encoder) -
                                    signedPortionBeginOffsetFromBack)
        signedPortionEndOffset = len(encoder) - signedPortionEndOffsetFromBack

        return (Blob(encoder.getOutput(), False), signedPortionBeginOffset,
                signedPortionEndOffset)

    @classmethod
    def get(self):
        """
        Get a singleton instance of a Tlv0_2WireFormat.  To always use the
        preferred version NDN-TLV, you should use TlvWireFormat.get().

        :return: The singleton instance.
        :rtype: Tlv0_2WireFormat
        """
        if self._instance == None:
            self._instance = Tlv0_2WireFormat()
        return self._instance
